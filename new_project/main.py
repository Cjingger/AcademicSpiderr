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
    PATH = "./static/EI期刊名-生物材料及医学.xlsx"
    name = "EI-bio-medical"
    DataUtil.load_index_data(PATH, name)

    # proj = "scopus"
    proj = "EI"
    # proj = "sci"
    cs = "s"
    start_year = 2018
    sid = "EUW1ED0F7FruOg9Uj0vlUwKaJsaMy"
    process_run(proj, cs, start_year, sid)


# See PyCharm help at https://www.jetbrains.com/help/pycharm/
