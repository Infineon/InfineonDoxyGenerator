import argparse, json, os, shutil, subprocess

doxygen_exe  = 'doxygen'
git_exe      = 'git'
grviz_exe    = 'dot'

grviz_enabled = True

global lib_root

lib_root  = './..'
docs_dir  = lib_root + '/docs'
img_dir   = lib_root + '/docs/img'
src_dir   = lib_root + '/src'
doxy_dir  = lib_root + '/docs/doxygen'
build_dir = lib_root + '/docs/doxygen/build'   


def get_toolchain_ver():

    """ 
    Gets the toolchain software versions 

    """

    git_exe     = 'git'
    doxygen_exe = 'doxygen'
    grviz_exe   = 'dot'

    return_sucesss = True

    print("Git      (required):")
    try:
        git_proc = subprocess.Popen([git_exe,'--version'])
        git_proc.wait()
    except:
        print('\'' + git_exe + '\'command is not recognized')
        return_sucesss = False

    print("Doxygen  (required):")
    try:
        doxy_proc = subprocess.Popen([doxygen_exe,'--version'])
        doxy_proc.wait()
    except:
        print('\'' + doxygen_exe + '\' command is not recognized')
        return_sucesss = False

    print('Graphviz (optional):')
    try:
        grviz_proc = subprocess.Popen([grviz_exe,'-V'])
        grviz_proc.wait()
    except:
        print('\'' + grviz_exe + '\' command is not recognized')
        grviz_enabled = False

    return return_sucesss

def get_lib_info_field(field_key):

    """
    Parses the requested field key from the library arduino manifest


    """
    field_value = ""
    print("library root : " + lib_root )
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
        prj_logo = './img/ifx_logo2.png'

    return prj_logo

def get_prj_mainpage():
    return ""

def doxyfile_config():
    doxyf_cfg = doxy_dir + "/doxyfile"
    # Check if doxyfile exist
    if os.path.exists(doxyf_cfg):
        print("doxyfile already exists. Using project custom doxyfile")
    else:
        doxyf_cfg = doxy_dir + "/doxyfile_auto"
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
            if grviz_enabled:
                auto_doxyf.write("HAVE_DOT               = YES\n")
                auto_doxyf.write("CALL_GRAPH             = YES\n")
                auto_doxyf.write("DOT_PATH               = " + "\"" + grviz_exe + "\"" + "\n")

        auto_doxyf.close()
        
    return doxyf_cfg

def generate_html():
    # Generate doxygen configuration file
    doxyf_cfg = doxyfile_config()
    # Generate doxygen
    doxy_proc = subprocess.Popen([doxygen_exe, doxyf_cfg])      
    doxy_proc.wait()
    

'''
Release on GitHub

'''

def get_repo_url_name():
    url_ifx_base_gh = 'https://github.com/infineon'
    git_proc = subprocess.Popen([git_exe, 'remote', '-v'], stdout=subprocess.PIPE)
    output, err = git_proc.communicate()
    git_proc.wait()
    output = str(output)
    url_ifx_repo_gh = output[output.index(url_ifx_base_gh):output.index('.git') + len('.git')]
    repo_name = output[output.index(url_ifx_base_gh) + len(url_ifx_base_gh):output.index('.git')]
    return repo_name, url_ifx_repo_gh

def clone_repo(repo_name, url):
    if not os.path.exists(repo_name):
        git_proc = subprocess.Popen([git_exe, 'clone', url])
        git_proc.wait()

def checkout_ghpages_branch():
    git_proc = subprocess.Popen([git_exe, 'branch', '-r'],stdout=subprocess.PIPE)
    output, err = git_proc.communicate()
    git_proc.wait()
    output = str(output)
    # If the branch does not exists needs to be created
    if output.find('origin/gh-pages') == -1:
        print("Github pages does not exist. Creating orphan branch.")
        git_proc2 = subprocess.Popen([git_exe, 'checkout', '--orphan', 'gh-pages'])
        git_proc2.wait()
    else:
        print("Github pages exists. Pulling and checking out to gh-pages.")
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
    global lib_root
    base_domain_gh = '@github.com/infineon/'
    git_proc  = subprocess.Popen([git_exe,'add','.'])
    git_proc.wait()
    # The lib root has changed
    lib_root = './../../'
    commit_msg = "\"Automated doxygen html release v" + get_prj_version() + "\""
    lib_root = './..'
    git_proc2 = subprocess.Popen([git_exe,'commit','-m',commit_msg])
    git_proc2.wait()
    url_with_cred = 'https://' + user + ':' + token + base_domain_gh + repo_name + '.git'
    git_proc3 = subprocess.Popen([git_exe,'remote','set-url','origin', url_with_cred])
    git_proc3.wait()
    git_proc4 = subprocess.Popen([git_exe,'push','origin','gh-pages'])  
    git_proc4.wait()

def release_html(user,passw):

    os.chdir(lib_root)

    # Get the target repository urlgit 
    repo_name, url_ifx_repo_gh = get_repo_url_name()

    os.chdir('./InfineonDoxyGenerator')
    # clone the original repository
    clone_repo(repo_name, url_ifx_repo_gh)

    os.chdir('./' + repo_name)
    # Look for gh-pages branch
    checkout_ghpages_branch()

    # rm any content that might exist
    remove_old()

    os.chdir('./../')
    # copy the html folder content
    copy_html(repo_name)

    os.chdir('./' + repo_name)
    # Push documentation and release under gh-pages
    git_push(user, passw, repo_name)

    os.chdir('./../')
    # rm original repository
    shutil.rmtree('./' + repo_name)


def clean_build():
    shutil.rmtree(build_dir)
    os.remove(doxy_dir + "/doxyfile_auto")

def get_cli_ver():
    """ 
    Gets the CLI version from the info.json manifests 
    """
    with open('./info.json') as lib_info:
        lib_info_json = json.load(lib_info)
        version = lib_info_json['version']
    lib_info.close()
    return 'v.' + version 


'''
Python Doxygen Documentation CLI Parser
'''

def parser_doxygen():

    def noarg(args):
        parser.print_help()

    def html(args):
        generate_html()
    
    def clean(args):
        clean_build()

    def tools(args):
        if args.version:
            get_toolchain_ver()
        elif args.install is not None:
            print("Installation still not available in version " + version() )

    def release(args):
        print(args.user)
        print(args.password)
        release_html(args.user, args.password)

    def version():
        return get_cli_ver()

    parser     = argparse.ArgumentParser(description="Infineon Doxygen Generator Python Command Line Interface")
    subparsers = parser.add_subparsers()
    parser.set_defaults(func=noarg)

    parser.add_argument('-v','--version', action='version', version='%(prog)s ' + version())

    parser_html = subparsers.add_parser('html', help='Generate html format')
    parser_html.set_defaults(func=html)

    parser_clean = subparsers.add_parser('clean', help='Clean build')
    parser_clean.set_defaults(func=clean)

    parser_tools = subparsers.add_parser('tools', help='Doxygen toolchain utility')
    parser_tools.add_argument('-i','--install', action='store', default='all', choices=['doxygen','graphviz','latex','all'], dest='install', help='Install Doxygen toolchain')
    parser_tools.add_argument('-v','--version', action='store_true', default=False, dest='version', help='Toolchain version')
    parser_tools.set_defaults(func=tools)

    parser_release = subparsers.add_parser('release', help='Release and publish documentation')
    parser_release.add_argument('user', type=str, help="Github user name")
    parser_release.add_argument('password', type=str, help="Github password or token")
    parser_release.set_defaults(func=release)
 
    args = parser.parse_args()
    args.func(args)

if __name__ == "__main__":
    parser_doxygen()

