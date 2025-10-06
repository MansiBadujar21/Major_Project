import json
import os
from typing import Dict, Optional, List
from datetime import datetime
from pathlib import Path


class EmployeeValidator:
    """Validates employee data against existing records with enhanced error handling"""
    
    def __init__(self):
        self.employees_file = Path(__file__).parent.parent / "data" / "employees.json"
        self._employees_data = None
    
    def _load_employees_data(self) -> List[Dict]:
        """Load employee data from JSON file with enhanced error handling"""
        if self._employees_data is None:
            try:
                if not self.employees_file.exists():
                    print(f"Warning: Employee data file not found at {self.employees_file}")
                    return []
                
                with open(self.employees_file, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                    if not isinstance(data, list):
                        print("Warning: Employee data file does not contain a list")
                        return []
                    self._employees_data = data
            except (FileNotFoundError, json.JSONDecodeError, PermissionError) as e:
                print(f"Error loading employee data: {str(e)}")
                return []
            except Exception as e:
                print(f"Unexpected error loading employee data: {str(e)}")
                return []
        return self._employees_data
    
    def validate_employee(self, employee_data: Dict) -> Dict:
        """
        Validate employee data against existing records - ALL fields must match exactly
        
        Args:
            employee_data: Dictionary containing employee information
            
        Returns:
            Dict with validation result and details
        """
        try:
            employees = self._load_employees_data()
            
            # Validate input
            if not employee_data or not isinstance(employee_data, dict):
                return {
                    'is_valid': False,
                    'employee_found': False,
                    'matched_employee': None,
                    'errors': ['Invalid employee data format'],
                    'warnings': []
                }
            
            # Extract search criteria with safe defaults and validation
            employee_name = str(employee_data.get('full_name', '')).strip()
            employee_id = str(employee_data.get('employee_code', '')).strip()
            designation = str(employee_data.get('designation', '')).strip()
            department = str(employee_data.get('department', '')).strip()
            joining_date = str(employee_data.get('joining_date', '')).strip()
            
            # Basic validation of required fields
            if not employee_name and not employee_id:
                return {
                    'is_valid': False,
                    'employee_found': False,
                    'matched_employee': None,
                    'errors': ['Either employee name or employee ID is required'],
                    'warnings': []
                }
            
            # Validation results
            validation_result = {
                'is_valid': False,
                'employee_found': False,
                'matched_employee': None,
                'errors': [],
                'warnings': []
            }
            
            # Find employee by ID first (most reliable)
            if employee_id:
                for emp in employees:
                    if emp and isinstance(emp, dict) and emp.get('employee_code', '').strip().upper() == employee_id.upper():
                        validation_result['employee_found'] = True
                        validation_result['matched_employee'] = emp
                        break
            
            # If not found by ID, try by name
            if not validation_result['employee_found'] and employee_name:
                for emp in employees:
                    if emp and isinstance(emp, dict) and emp.get('full_name', '').strip().lower() == employee_name.lower():
                        validation_result['employee_found'] = True
                        validation_result['matched_employee'] = emp
                        validation_result['warnings'].append(f"Employee found by name but ID doesn't match. Expected: {emp.get('employee_code')}")
                        break
            
            # If employee not found
            if not validation_result['employee_found']:
                validation_result['errors'].append(f"Employee not found in records. Please check the Employee ID or Name.")
                return validation_result
            
            # Validate against found employee record - ALL fields must match exactly
            matched_emp = validation_result['matched_employee']
            
            # Check employee name (case-insensitive)
            if employee_name and matched_emp.get('full_name', '').strip().lower() != employee_name.lower():
                validation_result['errors'].append(f"Employee name mismatch. Expected: {matched_emp.get('full_name')}, Provided: {employee_name}")
            
            # Check employee ID (case-insensitive)
            if employee_id and matched_emp.get('employee_code', '').strip().upper() != employee_id.upper():
                validation_result['errors'].append(f"Employee ID mismatch. Expected: {matched_emp.get('employee_code')}, Provided: {employee_id}")
            
            # Check designation (case-insensitive)
            if designation and matched_emp.get('designation', '').strip().lower() != designation.lower():
                validation_result['errors'].append(f"Designation mismatch. Expected: {matched_emp.get('designation')}, Provided: {designation}")
            
            # Check department (case-insensitive)
            if department and matched_emp.get('department', '').strip().lower() != department.lower():
                validation_result['errors'].append(f"Department mismatch. Expected: {matched_emp.get('department')}, Provided: {department}")
            
            # Check joining date (exact match)
            if joining_date:
                try:
                    # Parse provided date (expecting YYYY-MM-DD format from frontend)
                    provided_date = datetime.strptime(joining_date, '%Y-%m-%d').date()
                    
                    # Parse expected date (from database, could be DD-MM-YYYY or YYYY-MM-DD)
                    expected_date_str = matched_emp.get('joining_date', '')
                    try:
                        # Try YYYY-MM-DD format first
                        expected_date = datetime.strptime(expected_date_str, '%Y-%m-%d').date()
                    except ValueError:
                        try:
                            # Try DD-MM-YYYY format (database format)
                            expected_date = datetime.strptime(expected_date_str, '%d-%m-%Y').date()
                        except ValueError:
                            validation_result['errors'].append(f"Invalid expected date format in database: {expected_date_str}")
                            return validation_result
                    
                    if provided_date != expected_date:
                        validation_result['errors'].append(f"Joining date mismatch. Expected: {matched_emp.get('joining_date')}, Provided: {joining_date}")
                except ValueError:
                    validation_result['errors'].append(f"Invalid joining date format. Expected: YYYY-MM-DD, Provided: {joining_date}")
            
            # Check if employee is still active (not a future joining date)
            if joining_date:
                try:
                    # Parse provided date (expecting YYYY-MM-DD format from frontend)
                    joining_date_obj = datetime.strptime(joining_date, '%Y-%m-%d').date()
                    current_date = datetime.now().date()
                    
                    if joining_date_obj > current_date:
                        validation_result['warnings'].append("Joining date is in the future. Please verify the date.")
                except ValueError:
                    pass  # Already handled above
            
            # Set validation result - ALL fields must match for validation to pass
            validation_result['is_valid'] = len(validation_result['errors']) == 0
            
            return validation_result
            
        except Exception as e:
            print(f"Error in employee validation: {str(e)}")
            return {
                'is_valid': False,
                'employee_found': False,
                'matched_employee': None,
                'errors': [f'Validation error: {str(e)}'],
                'warnings': []
            }
    
    def get_employee_suggestions(self, partial_name: str, limit: int = 5) -> List[Dict]:
        """
        Get employee suggestions based on partial name match with enhanced error handling
        
        Args:
            partial_name: Partial name to search for
            limit: Maximum number of suggestions to return
            
        Returns:
            List of matching employees
        """
        try:
            employees = self._load_employees_data()
            suggestions = []
            
            if not partial_name or not isinstance(partial_name, str):
                return suggestions
            
            partial_name = partial_name.strip().lower()
            
            for emp in employees:
                if not isinstance(emp, dict):
                    continue
                    
                emp_name = str(emp.get('full_name', '')).lower()
                emp_id = str(emp.get('employee_code', '')).lower()
                
                if (partial_name in emp_name or 
                    partial_name in emp_id or 
                    any(word in emp_name for word in partial_name.split())):
                    suggestions.append({
                        'full_name': emp.get('full_name', ''),
                        'employee_code': emp.get('employee_code', ''),
                        'designation': emp.get('designation', ''),
                        'department': emp.get('department', ''),
                        'joining_date': emp.get('joining_date', '')
                    })
                    
                    if len(suggestions) >= limit:
                        break
            
            return suggestions
            
        except Exception as e:
            print(f"Error getting employee suggestions: {str(e)}")
            return []
    
    def get_employee_by_id(self, employee_id: str) -> Optional[Dict]:
        """
        Get employee by ID with enhanced error handling
        
        Args:
            employee_id: Employee ID to search for
            
        Returns:
            Employee data if found, None otherwise
        """
        try:
            if not employee_id or not isinstance(employee_id, str):
                return None
                
            employees = self._load_employees_data()
            
            for emp in employees:
                if not isinstance(emp, dict):
                    continue
                    
                if emp.get('employee_code', '').strip().upper() == employee_id.strip().upper():
                    return emp
            
            return None
            
        except Exception as e:
            print(f"Error getting employee by ID: {str(e)}")
            return None
