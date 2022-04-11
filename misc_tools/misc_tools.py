from pathlib import Path
import re
import shutil
import os

def copy_dependencies(file, src_folder, dest_folder):
    data = open(file, 'r').read()
    file_paths = re.findall('".{1,255}?"', data)
    file_paths = [re.sub('"', '', x) for x in file_paths]
    keep_file_exts = ['.css', '.js', '.svg', '.png']
    keep_file_exts = ['\\' + x for x in keep_file_exts]
    keep_file_exts = '|'.join(keep_file_exts)

    file_exts = []
    for x in file_paths:
        try:
            file_exts.append(re.search('\\..{1,5}',x).group(0))
        except:
            pass

    file_exts = list(set(file_exts))

    file_paths = [x for x in file_paths if bool(re.findall(keep_file_exts, x))]
    file_paths = [x for x in file_paths if x[0]!='.']

    file_paths = [re.sub('vendor/bulkit', '', x) for x in file_paths]

    # for x in file_paths:
    #     print(x)

    for x in file_paths:
        src = src_folder + x
        dst = dest_folder + x
        dst_subfolder = os.path.dirname(dst)
        Path(dst_subfolder).mkdir(parents=True, exist_ok=True)
        shutil.copyfile(src, dst)
        print(x)

if __name__ == '__main__':
    file = '/Users/rapple2018/Documents/Professional/Entrepreneur/Bill More Tech/bmt-sales-automation-saas/templates/web/components/bulkit_body.html'
    src_folder = '/Users/rapple2018/Documents/Professional/Entrepreneur/Bill More Tech/tools/themeforest-Y3pCVj8L-bulkit-agency-startup-and-saas-template/precompiled/assets/'
    dest_folder = '/Users/rapple2018/Documents/Professional/Entrepreneur/Bill More Tech/bmt-sales-automation-saas/static/vendor/bulkit'
    copy_dependencies(file, src_folder, dest_folder)