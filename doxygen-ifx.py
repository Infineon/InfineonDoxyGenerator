import argparse, os, shutil, subprocess

doxygen_exe  = 'doxygen'
git_exe      = 'git'

lib_root  = os.path.abspath(os.pardir)
docs_dir  = lib_root + '/docs'
img_dir   = lib_root + '/docs/img'
src_dir   = lib_root + '/src'
doxy_dir  = lib_root + '/docs/doxygen'
build_dir = lib_root + '/docs/doxygen/build'   

def get_os():
    pass

def check_new_tag():
    pass

def get_toolchain_ver():
    git_exe     = 'git'
    doxygen_exe = 'doxygen'
    latex_exe   = 'textlive'
    grviz_exe   = 'graphviz'
    print("Git      (required):")
    git_proc = subprocess.Popen([git_exe,'--version'])
    git_proc.wait()
    print("Doxygen  (required):")
    doxy_proc = subprocess.Popen([doxygen_exe,'--version'])
    doxy_proc.wait()
    print('Latex    (required for pdf):')
    latex_proc = subprocess.Popen([latex_exe,'version'])
    latex_proc.wait()
    print('Graphviz (optional):')
    grviz_proc = subprocess.Popen([grviz_exe,'version'])
    grviz_proc.wait()


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
    return get_lib_info_field('version')

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

def git_push(user,token, repo_name):

    git_proc  = subprocess.Popen([git_exe,'add','.'])
    git_proc.wait()
    commit_msg = "\"Automated doxygen html release v" + get_prj_version() + "\""
    git_proc2 = subprocess.Popen([git_exe,'commit','-m',commit_msg])
    git_proc2.wait()
    url_with_cred = 'https://' + user + ':' + token + '@github.com/infineon/' + repo_name + '.git'
    git_proc3 = subprocess.Popen([git_exe,'remote','set-url','origin', url_with_cred])
    git_proc3.wait()
    git_proc4 = subprocess.Popen([git_exe,'push','origin','gh-pages'])  
    git_proc4.wait()

def release_html(user,passw):

    os.chdir(lib_root)

    # Get the target repository urlgit 
    repo_name, url_ifx_repo_gh = get_repo_url_name()

    #os.chdir('./InfineonDoxyGenerator')
    # clone the original repository
    #clone_repo(url_ifx_repo_gh)

    #os.chdir('./' + repo_name)
    # Look for gh-pages branch
    #checkout_ghpages_branch()

    # rm any content that might exist
    #remove_old()

    #os.chdir('./../')
    # copy the html folder content
    #copy_html(repo_name)

    #os.chdir('./' + repo_name)
    # Push documentation and release under gh-pages
    #git_push(user, passw, repo_name)

    #os.chdir('./../')
    # rm original repository
    #shutil.rmtree('./' + repo_name)


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

    def html(args):
        print("html parser")
        generate_html()
    
    def pdf(args):
        print("PDF generation NOT available :(")
        generate_pdf()
    
    def clean(args):
        print("clean parser")
        clean()

    def tools(args):
        print("tools parser")
        if args.version:
            get_toolchain_ver()
        elif args.install is not None:
            print("installation required of not none")

    def release(args):
        print("release parser")
        print(args.user)
        print(args.password)
        print(args.format)
        release_html(args.user, args.password)

    def version():
        return "this is the version of this program"

    parser    = argparse.ArgumentParser(description="Infineon Doxygen Generator Python Command Line")
    subparsers = parser.add_subparsers()
        
    parser.add_argument('-v','--version', action='version', version='%(prog)s ' + version())

    parser_html = subparsers.add_parser('html', help='Generate html format')
    parser_html.set_defaults(func=html)

    parser_pdf = subparsers.add_parser('pdf', help='Generate pdf format')
    parser_pdf.set_defaults(func=pdf)

    parser_clean = subparsers.add_parser('clean', help='Clean build')
    parser_clean.set_defaults(func=clean)

    parser_tools = subparsers.add_parser('tools', help='Doxygen toolchain utility')
    parser_tools.add_argument('-i','--install', action='store', default='all', choices=['doxygen','graphviz','latex','all'], dest='install', help='Install Doxygen toolchain')
    parser_tools.add_argument('-v','--version', action='store_true', default=False, dest='version', help='Toolchain version')
    parser_tools.set_defaults(func=tools)

    parser_release = subparsers.add_parser('release', help='Release and publish documentation')
    parser_release.add_argument('user', type=str, help="Github user name")
    parser_release.add_argument('password', type=str, help="Github password or token")
    parser_release.add_argument('format', action='store', nargs='?', type=str, choices=['html','pdf','all'], default='all', help='Documentation Release Format')
    parser_release.set_defaults(func=release)
 
    args = parser.parse_args()
    args.func(args)

if __name__ == "__main__":
    parser_doxygen()
