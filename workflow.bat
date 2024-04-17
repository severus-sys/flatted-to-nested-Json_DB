
@echo off
py "%~dp0get_json_and_fix.py"
py "%~dp0get_data_json.py"
py "%~dp0convert_flatten.py"
py "%~dp0insert_data_to_pg.py"
echo Workflow completed.

