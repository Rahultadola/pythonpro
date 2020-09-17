ratio_dict = [
    {
        'ratio': '854x480',
        'bitrate': '768k',
        'name_of_file':'',
    },
    {
        'ratio': '640x360',
        'bitrate': '512k',
        'video480':'',
    },
    {
        'ratio': '320x180',
        'bitrate': '256k',
        'video240':'',
    }
]

for i in range(3):
    ratio_dict[i]['name_of_file'] = title +'_' + ratio_dict[i]['ratio'][-3:] + '.mp4'
    out_path = os.path.join(fp, name_of_file)

    cmd = ['ffmpeg','-y', '-i', last_saved, '-s', ratio_dict[i]['ratio'],'-b:v', ratio_dict[i]['bitrate'], '-c:a', 'aac','-b:a', '64k', out_path]
            subprocess.check_output(cmd, shell = True)
            last_saved = ''+out_path 
            path_480 = last_saved

        elif (ratio =='640x360') :
            name_of_file = title +'_240' + '.mp4'
            out_path = os.path.join(fp, name_of_file)
            video480 = name_of_file
            cmd = ['ffmpeg','-y', '-i', last_saved, '-s', ratio, '-b:v', '512k', '-c:a', 'aac','-b:a', '64k',out_path]
            subprocess.check_output(cmd, shell = True)
            last_saved = ''+out_path
        
