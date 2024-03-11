# This is a sample Python script.

# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.
from subprocess import run, Popen
import traceback
from common.common_utils import DataUtil


def print_hi(name):
    # Use a breakpoint in the code line below to debug your script.
    print(f'Hi, {name}')  # Press Ctrl+F8 to toggle the breakpoint.


def process_run(proj: str, cs: str, start_year: int, sid: str):
    try:
        cmd = r'python E:/project/new_project/make_args.py --proj="{}" --cs="{}" --start_year="{}" --sid="{}"'. \
            format(proj, cs, start_year, sid)
        completed = run(cmd, shell=True, check=True)
        return completed
    except:
        traceback.print_exc()

# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    PATH = "./static/energy-SCI-10.17.xlsx"
    name = "SCI-10-17"
    # DataUtil.load_index_data(PATH, name)

    # proj = "scopus"
    # proj = "EI"
    proj = "sci"
    cs = "c"
    start_year = 2018
    sid = "USW2EC0A7FgPiEtmTpluYMkYfb5Pa"
    process_run(proj, cs, start_year, sid)


# See PyCharm help at https://www.jetbrains.com/help/pycharm/
