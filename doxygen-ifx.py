import argparse, os, shutil, subprocess

doxygen_exe  = 'doxygen'
git_exe      = 'git'

lib_root  = './..'
docs_dir  = lib_root + '/docs'
img_dir   = lib_root + '/docs/img'
src_dir   = lib_root + '/src'
doxy_dir  = lib_root + '/docs/doxygen'
build_dir = lib_root + '/docs/doxygen/build'   

global lib_version 

def get_os():
    pass

def check_new_tag():
    pass

def get_toolchain_ver():
    git_exe     = 'git'
    doxygen_exe = 'doxygen'
    # latex_exe   = 'textlive'
    # grviz_exe   = 'graphviz'
    git_proc = subprocess.Popen([git_exe,'--version'])
    git_proc.wait()
    doxy_proc = subprocess.Popen([doxygen_exe,'--version'])
    doxy_proc.wait()
    # latex_proc = subprocess.Popen([latex_exe,'version'])
    # latex_proc.wait()
    # grviz_proc = subprocess.Popen([grviz_exe,'version'])
    # grviz_proc.wait()

def toolchain_install():
    pass
    # if linux
    # if windows
    # if minwg

def get_lib_info_field(field_key):
    field_value = ""
    if os.path.exists(lib_root + "/library.properties"):
        with open(lib_root + '/library.properties','r') as prj_file:
            prj_info = prj_file.readlines()
            for line in prj_info:
                if line.find(field_key + "=") == 0:
                    field_value = line[len(field_key + "="):line.index('\n')]
        prj_file.close()
    else:
        print("Library info manifest NOT found")

    if field_value is "":
        print("Field value NOT found")

    return field_value

def get_prj_name():
    return  "\"" + get_lib_info_field('name').replace('-',' ') + "\""
    
def get_prj_version():
    global lib_version
    lib_version = get_lib_info_field('version')
    return lib_version

def get_prj_descr():
    return "\"" + get_lib_info_field('paragraph') + "\""

def get_prj_input():
    # Add custom project doxy files
    prj_input = ""
    # Add doxygen files from project if existing
    if os.path.exists(doxy_dir):
        prj_input += doxy_dir

    prj_input += '  ' + src_dir #+ '  ./latexfiles'
    
    return prj_input

def get_prj_logo():
    prj_logo = ""
    # If custom logo exists
    if os.path.exists(img_dir + '/lib_logo.png'):
        prj_logo = img_dir + '/lib_logo.png'
    else:
        # Default infineon logo
        prj_logo = './docs/img/ifx_logo2.png'

    return prj_logo

def get_prj_mainpage():
    return ""

def doxyfile_config():
    doxyf_cfg = doxy_dir + "/doxyfile"
    # Check if doxyfile exist
    if os.path.exists(doxyf_cfg):
        print("doxyfile already exists. Using project custom doxyfile")
    else:
        if not os.path.exists(doxy_dir):
            os.makedirs(doxy_dir)

        with open(doxyf_cfg,'w+') as auto_doxyf:
            auto_doxyf.write("PROJECT_NAME           = " + get_prj_name() + "\n")
            auto_doxyf.write("PROJECT_NUMBER         = " + get_prj_version() + "\n")
            auto_doxyf.write("PROJECT_BRIEF          = " + get_prj_descr() + "\n")
            auto_doxyf.write("OUTPUT_DIRECTORY       = " + build_dir + "\n")
            auto_doxyf.write("CREATE_SUBDIRS         = YES\n")
            auto_doxyf.write("EXTRACT_ALL            = YES\n")
            auto_doxyf.write("INPUT                  = " + get_prj_input() + "\n")
            auto_doxyf.write("RECURSIVE              = YES\n")
            auto_doxyf.write("USE_MDFILE_AS_MAINPAGE = " + get_prj_mainpage() + "\n")
            auto_doxyf.write("DISABLE_INDEX          = YES\n")
            auto_doxyf.write("GENERATE_TREEVIEW      = YES\n")
            auto_doxyf.write("PROJECT_LOGO           = " + get_prj_logo() + "\n")
            auto_doxyf.write("GENERATE_TODOLIST      = NO\n")        
            auto_doxyf.write("IMAGE_PATH             = \n" )
            auto_doxyf.write("GENERATE_LATEX         = NO\n" )
            auto_doxyf.write("WARN_LOGFILE           = " + build_dir + "/doxygen-log.txt\n" )
        auto_doxyf.close()
        
    return doxyf_cfg

def generate_html():
    # Generate doxygen configuration file
    doxyf_cfg = doxyfile_config()
    # Generate doxygen
    doxy_proc = subprocess.Popen([doxygen_exe, doxyf_cfg])      
    doxy_proc.wait()
    
def get_repo_url_name():
    url_ifx_base_gh = 'https://github.com/jaenrig/' #'https://github.com/infineon'
    git_proc = subprocess.Popen([git_exe, 'remote', '-v'], stdout=subprocess.PIPE)
    output, err = git_proc.communicate()
    git_proc.wait()
    url_ifx_repo_gh = output[output.index(url_ifx_base_gh):output.index('.git') + len('.git')]
    repo_name = output[output.index(url_ifx_base_gh) + len(url_ifx_base_gh):output.index('.git')]
    return repo_name, url_ifx_repo_gh

def clone_repo(url):
    git_proc = subprocess.Popen([git_exe, 'clone', url])
    git_proc.wait()

def checkout_ghpages_branch():

    git_proc = subprocess.Popen([git_exe, 'branch', '-r'],stdout=subprocess.PIPE)
    output, err = git_proc.communicate()
    git_proc.wait()
    print("output: " + output)
    # If the branch does not exists needs to be created
    if output.find('origin/gh-pages') == -1:
        print("Github pages does not exist. Creating orphan branch.")
        git_proc2 = subprocess.Popen([git_exe, 'checkout', '--orphan', 'gh-pages'])
        git_proc2.wait()
    else:
        print("github pages exists. Pulling and checking out to gh-pages.")
        git_proc3 = subprocess.Popen([git_exe, 'pull', 'origin', 'gh-pages'])
        git_proc3.wait()
        git_proc4 = subprocess.Popen([git_exe, 'checkout', 'gh-pages'])
        git_proc4.wait()

def remove_old():
    git_proc = subprocess.Popen([git_exe, 'rm', '-rf', '*'])
    git_proc.wait()

    dir_content = os.listdir('./')
    dir_content.remove('.git')
    if os.path.exists('./.gitignore'):
        dir_content.remove('.gitignore')

    for item in dir_content:
        if os.path.isdir(item):
            shutil.rmtree(item)
        elif os.path.isfile(item):
            os.remove(item)

def copy_html(repo_name):

    src_dir  = build_dir + '/html'
    dest_dir = lib_root + '/InfineonDoxyGenerator/' + repo_name
    dir_content = os.listdir(src_dir)

    for item in dir_content:
        src  = os.path.join(src_dir, item)
        dest = os.path.join(dest_dir, item) 
        if os.path.isdir(src):
            shutil.copytree(src, dest)
        if os.path.isfile(src):
            shutil.copy2(src, dest)

def release_html():

    os.chdir(lib_root)
    # Get the target repository urlgit 
    repo_name, url_ifx_repo_gh = get_repo_url_name()

    os.chdir('./InfineonDoxyGenerator')
    # clone the original repository
    #clone_repo(url_ifx_repo_gh)

    os.chdir('./' + repo_name)
    # Look for gh-pages branch
    #checkout_ghpages_branch()

    # rm any content that might exist
    #remove_old()

    os.chdir('./../')
    # copy the html folder content
    copy_html(repo_name)

    # cp docs/doxygen/build/html ./

    #os.chdir('./' + repo_name)
    # git commit -m "Automated doxygen release version"
    # handle credentials!!
    # git push
    # cd out of repository
    # rm
    # rm original repository

def generate_pdf():
    pass
    # Generate pdf under docs. It is up to the user 
    # to store it there or not

def release_pdf():
    pass

def clean():
    shutil.rmtree(build_dir)
    os.remove(doxy_dir + "/doxyfile")

def parser_doxygen():
    parser = argparse.ArgumentParser(description="Infineon Doxygen Generator Python Command Line")
    parser.add_argument('--html', action='store_true', default=False, dest='gen_html', help='Generate html format')
    parser.add_argument('--pdf', action='store_true', default=False, dest='gen_pdf', help='Generate pdf format')
    parser.add_argument('--tool', action='store_true', default=False, dest='toolchain_cmd', help='Check doxygen toolchain version')
    parser.add_argument('--version', action='version', version='%(prog)s 1.0.0')
    parser.add_argument('--clean', action='store_true', default=False, dest='clean_cmd', help='Clean build')
    parser.add_argument('--release', action='store_true', default=False, dest='release_cmd', help='Release documentation')
 
    parser_out = parser.parse_args()
    if parser_out.gen_html :
        generate_html()
    if parser_out.clean_cmd :
        clean()
    if parser_out.toolchain_cmd:
        get_toolchain_ver()
    if parser_out.release_cmd:
        release_html()

if __name__ == "__main__":
    parser_doxygen()
    #checkout_ghpages_branch()