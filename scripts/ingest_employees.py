"""Ingest employees CSV and write backend/app/data/employees.json.

Usage:
  python scripts/ingest_employees.py org_data/employees.csv
"""
from __future__ import annotations

import csv
import json
import sys
from pathlib import Path
import re


REQUIRED_FIELDS = [
    "emp_id",
    "full_name",
    "designation",
    "department",
    "joining_date",
    "employee_code",
    "email",
]

# Support alternate header names from real-world datasets
ALT_HEADERS = {
    "emp_id": ["emp_id", "employee_id", "EmployeeID", "EmpID", "Emp_Id"],
    "full_name": ["full_name", "name", "Name", "Full Name"],
    "designation": ["designation", "Designation", "Title", "Role"],
    "department": ["department", "Department", "Dept"],
    "joining_date": ["joining_date", "JoiningDate", "DateOfJoining", "DOJ", "StartDate"],
    "employee_code": ["employee_code", "EmployeeCode", "EmpCode", "Code"],
    "email": ["email", "Email", "EmailID", "EmailId"],
}

def find_col(fieldnames: list[str], candidates: list[str]) -> str | None:
    lower = {f.lower(): f for f in fieldnames}
    for c in candidates:
        if c.lower() in lower:
            return lower[c.lower()]
    return None


def main(csv_path: str) -> None:
    src = Path(csv_path)
    if not src.exists():
        raise SystemExit(f"CSV not found: {src}")

    rows = []
    with src.open("r", encoding="utf-8-sig", newline="") as f:
        reader = csv.DictReader(f)
        if not reader.fieldnames:
            raise SystemExit("CSV has no headers")

        # Build a column map using ALT_HEADERS
        colmap: dict[str, str] = {}
        for key, candidates in ALT_HEADERS.items():
            colname = find_col(reader.fieldnames, candidates)
            if colname:
                colmap[key] = colname

        # Ensure we have minimum required logical fields (emp_id, full_name, designation, department, joining_date, email)
        logical_required = ["emp_id", "full_name", "designation", "department", "joining_date", "email"]
        missing_logical = [k for k in logical_required if k not in colmap]
        if missing_logical:
            raise SystemExit(f"CSV missing required columns (any alias accepted): {missing_logical}\nFound headers: {reader.fieldnames}")
        for r in reader:
            # Normalize and cast types
            try:
                emp_id_str = (r.get(colmap["emp_id"], "") or "").strip()
                try:
                    emp_id = int(emp_id_str)
                except ValueError:
                    digits = re.findall(r"\d+", emp_id_str)
                    if not digits:
                        raise ValueError(f"emp_id lacks digits: {emp_id_str}")
                    emp_id = int("".join(digits))

                full_name = (r.get(colmap["full_name"], "") or "").strip()
                designation = (r.get(colmap["designation"], "") or "").strip()
                department = (r.get(colmap["department"], "") or "").strip()
                joining_date = (r.get(colmap["joining_date"], "") or "").strip()
                email = (r.get(colmap["email"], "") or "").strip()

                # Employee code: use provided if present; else generate EMP{emp_id}
                if "employee_code" in colmap:
                    employee_code = (r.get(colmap["employee_code"], "") or "").strip() or emp_id_str or f"EMP{emp_id}"
                else:
                    # If original had non-digit prefix like EMP0001, keep it as code; else generate
                    employee_code = emp_id_str if not emp_id_str.isdigit() and emp_id_str else f"EMP{emp_id}"

                rows.append({
                    "emp_id": emp_id,
                    "full_name": full_name,
                    "designation": designation,
                    "department": department,
                    "joining_date": joining_date,
                    "employee_code": employee_code,
                    "email": email,
                })
            except Exception as e:
                raise SystemExit(f"Invalid row: {r}\nError: {e}")

    out = Path(__file__).resolve().parents[1] / "backend" / "app" / "data" / "employees.json"
    out.parent.mkdir(parents=True, exist_ok=True)
    with out.open("w", encoding="utf-8") as f:
        json.dump(rows, f, ensure_ascii=False, indent=2)
    print(f"Wrote {len(rows)} employees to {out}")


if __name__ == "__main__":
    if len(sys.argv) < 2:
        raise SystemExit("Usage: python scripts/ingest_employees.py org_data/employees.csv")
    main(sys.argv[1])


