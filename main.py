import argparse
import subprocess
import os

CLANG_DIR = "llvm-project"

def build_clang(clang_release, build_dir, c_compiler, cxx_compiler):
    subprocess.check_call(f"git checkout {clang_release}", shell=True)
    subprocess.check_call(f"cmake -S llvm "
                          f"-B {build_dir} "
                          f"-G \"Unix Makefiles\" "
                          f"-DLLVM_ENABLE_PROJECTS=\"clang\" "
                          f"-DCMAKE_BUILD_TYPE=Release "
                          f"-DCMAKE_C_COMPILER=\"{c_compiler}\" "
                          f"-DCMAKE_CXX_COMPILER=\"{cxx_compiler}\"", shell=True)
    os.chdir(build_dir)
    subprocess.check_call(f"make clang", shell=True)
    os.chdir("..")

if __name__ == '__main__':
    print("Kotlin/Native: musl-based target\n")

    parser = argparse.ArgumentParser()
    parser.add_argument("--clang_release", type=str, default="release/13.x", help="The clang target version.")
    args = parser.parse_args()
    if not os.path.exists(CLANG_DIR):
        subprocess.check_call(f"git clone https://github.com/llvm/llvm-project.git {CLANG_DIR}", shell=True)
    os.chdir(CLANG_DIR)

    #build by default compiler
    build_clang(args.clang_release, "build_1", "gcc", "g++")

    #rebuild by clang
    build_clang(args.clang_release, "build_2", f"{os.getcwd()}/build/bin/clang", f"{os.getcwd()}/build/bin/clang++")
