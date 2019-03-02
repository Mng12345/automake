# 自动生成makefile文件
import os
import sys
from typing import List


# 解析一个文件的头文件列表
def parse_includes(file: str)-> List[str]:
    res: List[str] = []
    if "\\" in file:
        file: str = file.replace("\\", "/")
    file_name = file.split("/")[-1]
    if "/" in file:
        cwd: str = "/".join(file.split("/")[:-1]) + "/"
    else:
        cwd: str = "./"
    with open(cwd + file_name, "r", encoding="utf-8") as f:
        for line in f:
            if "#include" in line and '"' in line:
                # 提取包含的文件
                line = line.strip()
                temp_include: str = line[line.index('"') + 1: -1]
                if ("\\") in temp_include:
                    temp_include = temp_include.replace("\\\\", "/")
                if "/" not in temp_include:
                    # 当前路径下
                    temp_include = cwd + temp_include
                res.append(temp_include)
    return res


# 生成make_file
def makefile(main_file: str, curr_file:str, make_file: List[str], debug: bool):
    # 获取make_file的includes
    includes: List[str] = parse_includes(curr_file)
    main_file_name = main_file.split("/")[-1].split(".")[0]
    curr_file_name = curr_file.split("/")[-1].split(".")[0]
    curr_file_path = "/".join(curr_file.split("/")[:-1]) + "/"
    if main_file == curr_file:
        cmd1 = main_file_name + ": " + main_file_name + ".o "
        if debug:
            cmd2 = "\tgcc -g -o " + main_file_name + " " + main_file_name + ".o "
        else:
            cmd2 = "\tgcc -o " + main_file_name + " " + main_file_name + ".o "
        for include in includes:
            include_name = include.split("/")[-1].split(".")[0]
            cmd1 += include_name + ".o "
            cmd2 += include_name + ".o "
        make_file.append(cmd1)
        make_file.append(cmd2)
        cmd1 = main_file_name + ".o: " + main_file_name + ".c "
        if debug:
            cmd2 = "\tgcc -g -c " + main_file_name + ".c "
        else:
            cmd2 = "\tgcc -c " + main_file_name + ".c "
        for include in includes:
            cmd1 += include + " "
        make_file.append(cmd1)
        make_file.append(cmd2)
    else:
        cmd1 = curr_file_name + ".o: " + \
               curr_file_path + curr_file_name + ".c "
        if debug:
            cmd2 = "\tgcc -g -c " + curr_file_path + curr_file_name + ".c"
        else:
            cmd2 = "\tgcc -c " + curr_file_path + curr_file_name + ".c"
        for include in includes:
            if "/" not in include:
                # include位于curr_file_path下
                cmd1 += curr_file_path + include + " "
            else:
                cmd1 += include + " "
        make_file.append(cmd1)
        make_file.append(cmd2)

    for include in includes:
        if curr_file_name in include:
            continue
        # 把所有.h换成.c
        include = include.replace(".h", ".c")
        makefile(main_file, include, make_file, debug)


def save_makefile(make_file: List[str], path: str):
    if os.path.exists(path):
        os.remove(path)
    with open(path, "w", encoding="utf-8") as f:
        for line in make_file:
            f.write(line + "\n")


if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("参数个数错误，需指定待解析主文件")
        sys.exit(-1)
    main_file: str = sys.argv[1]
    output_file: str = sys.argv[2]
    curr_file: str = main_file
    make_file: List[str] = []
    debug: bool = True
    makefile(main_file=main_file, curr_file=curr_file,
             make_file=make_file, debug=debug)
    for file in make_file:
        print(file)
    save_makefile(make_file=make_file, path=output_file)