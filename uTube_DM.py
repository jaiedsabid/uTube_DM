#!/usr/bin/env python3
import os
import re
import platform

from pytube import YouTube


# Global variables
fileSize = 0


def checkWindowsDrive(DriveLetter: str) -> bool:
    '''
    Check if windows drive letter is correct or not.
    '''
    DriveLetter = DriveLetter + ':\\'
    return os.path.isdir(DriveLetter)


def progress(chunk: bytes, file_handler, bytes_remaining: int):
    '''
        It will show how much completed downloading.
    '''
    global fileSize
    remaining = (100 * bytes_remaining) / fileSize
    step = 100 - int(remaining)
    print(f'Completed {step}%', end='\r')


def main():
    global fileSize
    vRes_pat = r'res=\"([\d\w]+)\"'
    while(True):
        if platform.system() == 'Windows':
            print('---------------------------------------------------')
            print('Enter the drive letter where video will be saved')
            print('---------------------------------------------------')
            drivePath = str(input('=> '))
            save_path = '<DRIVE_LETTER>:\\uTube_DM'
            if checkWindowsDrive(drivePath.upper()):
                save_path = save_path.replace(
                    '<DRIVE_LETTER>', str(drivePath.upper()))
                break
            else:
                print(
                    '\nInvalid drive location!\nPlease enter a valid drive location.\n')
        elif platform.system() == 'Linux':
            save_path = '/home/<USER>/Downloads'.replace(
                '<USER>', os.getlogin())
            break
    while(True):
        vResNvideos = {}
        vRes_list = []
        print('\n---------------------------------------------------')
        print('Enter video url or \"exit\" to exit the program')
        print('---------------------------------------------------\n')
        url_ = str(input('=> '))
        if(url_.lower() != 'exit'):
            try:
                videos_ = YouTube(url=url_, on_progress_callback=progress).streams.filter(
                    progressive=True)
                print('\n---------------------------------------------------')
                print('Available video resolutions')
                print('---------------------------------------------------\n')
                opRes = 1
                for video_ in videos_:
                    vRes = re.findall(vRes_pat, str(video_))
                    vResNvideos[str(vRes[0])] = video_
                    vRes_list.append(str(vRes[0]))
                    # Print available resulation and file size
                    print('{0}) {1} - {2:.1f} MB'.format(opRes,
                                                         vRes[0], vResNvideos[vRes[0]].filesize/2**20))
                    opRes += 1
                print('\n---------------------------------------------------')
                print(
                    'Choose video resulation from the available list\nex. 1 for 720p etc.')
                print('---------------------------------------------------\n')
                try:
                    opRes = int(input('=> '))
                    print()
                    # FileSize variable for Progress status
                    fileSize = vResNvideos[vRes_list[opRes-1]].filesize
                    vResNvideos[vRes_list[opRes-1]].download(save_path)
                    print('\nFile saved at', save_path)
                except (ValueError, IndexError) as errorCode:
                    print('\nInvalid input!\nReturned to main menu.')
            except Exception as e:
                print('\nInvalid URL!', e)
        elif(url_.lower() == 'exit'):
            print('\nExit successfully!')
            break


if __name__ == '__main__':
    main()
