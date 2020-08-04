import os
import re

from pytube import YouTube


def main():
    vRes_pat = r'res=\"([\d\w]+)\"'
    print('---------------------------------------------------')
    print('Enter the drive letter where video will be saved')
    print('---------------------------------------------------')
    save_path = '<DRIVE_LETTER>:\\uTube_DM'.replace('<DRIVE_LETTER>',
                                                    str(input('=> ').upper()))
    while(True):
        vResNvideos = {}
        vRes_list = []
        print('\n---------------------------------------------------')
        print('Enter video url or \"exit\" to exit the program')
        print('---------------------------------------------------\n')
        url_ = str(input('=> '))
        if(url_.lower() != 'exit'):
            videos_ = YouTube(url=url_).streams.filter(progressive=True)
            print('\n---------------------------------------------------')
            print('Available video resolutions')
            print('---------------------------------------------------\n')
            opRes = 1
            for video_ in videos_:
                vRes = re.findall(vRes_pat, str(video_))
                vResNvideos[str(vRes[0])] = video_
                vRes_list.append(str(vRes[0]))
                print('{0}) {1}'.format(opRes, vRes[0]))
                opRes += 1
            print('\n---------------------------------------------------')
            print('Choose video resulation from the available list\nex. 1 for 720p etc.')
            print('---------------------------------------------------\n')
            opRes = int(input('=> '))
            vResNvideos[vRes_list[opRes-1]].download(save_path)
            print('\nFile saved at', save_path)
        elif(url_.lower() == 'exit'):
            print('Exit successfully!')
            break
        else:
            print('Wrong input.')


if __name__ == '__main__':
    main()
