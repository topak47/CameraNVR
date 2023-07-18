# 引用模块
from bypy import ByPy     #百度网盘第三方API  开源地址：https://github.com/houtianze/bypy
from aligo import Aligo   #阿里云盘盘第三方API  开源地址：https://github.com/foyoux/aligo
import os
import cv2
import time
import threading

# 配置

Networkdisk = [1]  # 选择网盘 ([1] 表示百度网盘；[2] 表示阿里云网盘；[1, 2]同时选择两个网盘，)
Cameraname = 'videos'  # 摄像头名称
videopath = '/Camera/'  # 本地文件路径
NVRurl = '根据摄像头填写'  # 视频流URL 
videotime = 1  # 录制视频时长（分钟，范围：1-1000）
Updisk = True  # 是否上传到网盘？（True 表示上传；False 表示不上传）
deletevd = True  # 上传后是否删除视频文件？（True 表示删除；False 表示保留）
motion_frame_interval = 3  # 背景减除帧间隔
Networkdisk_space_threshold = 500  # 网盘剩余空间阈值（GB）
upload_threshold = 500  # 视频上传总大小阈值（GB）

# 获取文件上传的总大小
def get_uploaded_size():
    total_size = 0
    for root, dirs, files in os.walk(videopath):
        for file in files:
            total_size += os.path.getsize(os.path.join(root, file))
    return total_size

def bysync(file, path, i, deletevd):
    if i >= 3:
        print(file + " 上传错误，请检查网络、网盘账户和路径。")
        return
    time.sleep(10)
    print(file + " 正在上传到百度网盘......")
    bp = ByPy()
    code = bp.upload(file, '/' + path + '/', ondup='overwrite')  # 使用覆盖上传方式
    if code == 0:
        if deletevd:
            os.remove(file)
        print(file + " 上传成功！")
    else:
        i += 1
        print(file + " 重试次数: " + str(i))
        bysync(file, path, i, deletevd)

def alisync(file, path, i, deletevd):
    if i >= 3:
        print(file + " 上传错误，请检查网络、网盘账户和路径。")
        return
    time.sleep(10)
    print(file + " 正在上传到阿里云网盘......")
    ali = Aligo()
    code = ''
    global floder_id
    try:
        code = ali.upload_files(file_paths=[file], parent_file_id=floder_id, overwrite=True)  # 使用覆盖上传方式
    except Exception as e:
        print(e)
        i += 1
        print(file + " 重试次数: " + str(i))
        alisync(file, path, i, deletevd)
    if code != '':
        if deletevd:
            os.remove(file)
        print(file + " 上传成功！")
    else:
        i += 1
        print(file + " 重试次数: " + str(i))
        alisync(file, path, i, deletevd)

def capture(NVRurl, Cameraname, videopath, videotime, Updisk, deletevd, Networkdisk, Networkdisk_space_threshold, upload_threshold):
    try:
        print("****")
        cap = cv2.VideoCapture(NVRurl)
        print("****")
    except:
        print("无法捕获视频流，请检查URL或网络连接。")
        return

    fourcc = cv2.VideoWriter_fourcc(*'XVID')
    fps = int(cap.get(cv2.CAP_PROP_FPS))
    if fps >= 30:
        fps = 30
    elif fps <= 0:
        fps = 15
    print("fps: " + str(fps))
    size = (int(cap.get(cv2.CAP_PROP_FRAME_WIDTH)), int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT)))
    print("视频尺寸: " + str(size))
    videopath = os.path.join(videopath, Cameraname)
    if not os.path.exists(videopath):
        try:
            os.makedirs(videopath)
        except:
            print("请手动创建文件夹")
            return

    # 初始化视频上传总大小变量
    video_total_size = 0

    def alisync(file, path, i, deletevd):
        if i >= 3:
            print(file + " 上传错误，请检查网络、网盘账户和路径。")
            return
        time.sleep(10)
        print(file + " 正在上传到阿里云网盘......")
        ali = Aligo()
        code = ''
        global floder_id
        try:
            code = ali.upload_files(file_paths=[file], parent_file_id=floder_id, overwrite=True)  # 使用覆盖上传方式
        except Exception as e:
            print(e)
            i += 1
            print(file + " 重试次数: " + str(i))
            alisync(file, path, i, deletevd)
        if code != '':
            if deletevd:
                os.remove(file)
            print(file + " 上传成功！")
        else:
            i += 1
            print(file + " 重试次数: " + str(i))
            alisync(file, path, i, deletevd)

    # 检测网盘空间并删除早期上传的视频文件
    def check_and_delete_earlier_videos():
        nonlocal video_total_size
        if Updisk and 1 in Networkdisk and video_total_size > 0:  # 确保文件非空才进行上传判断
            uploaded_size = get_uploaded_size() / (1024 * 1024 * 1024)  # 转换为GB单位
            if uploaded_size > Networkdisk_space_threshold:
                print("上传视频总大小达到 {}GB，开始检查网盘剩余空间...".format(uploaded_size))
                bp = ByPy()
                space_info = bp.info()
                free_space = space_info['free'] / (1024 * 1024 * 1024)  # 转换为GB单位
                print("网盘剩余空间为 {}GB".format(free_space))
                if free_space < Networkdisk_space_threshold:
                    print("网盘剩余空间不足 {}GB，开始删除早期上传的视频文件...".format(Networkdisk_space_threshold))
                    # 删除早期上传的视频文件
                    files_to_delete = os.listdir(videopath)
                    files_to_delete.sort()
                    for file in files_to_delete:
                        file_path = os.path.join(videopath, file)
                        if os.path.isfile(file_path):
                            os.remove(file_path)
                            print("已删除文件：", file)
                    print("删除早期视频文件完成。")
        video_total_size = 0  # 清零视频总大小，为下一轮上传准备

    bg_subtractor = cv2.createBackgroundSubtractorKNN()

    frame_counter = 0

    while True:
        ret, frame = cap.read()
        if not ret:
            break

        frame_counter += 1
        if frame_counter % motion_frame_interval != 0:
            continue

        fg_mask = bg_subtractor.apply(frame)
        motion_pixels = cv2.countNonZero(fg_mask)

        if motion_pixels > 3000:
            print("检测到运动，开始录制视频...")
            cu_videopath = os.path.join(videopath, str(time.strftime("%Y-%m-%d-%H-%M-%S", time.localtime())) + '.avi')
            out = cv2.VideoWriter(cu_videopath, fourcc, fps, size)

            start_time = time.time()

            while True:
                ret, frame = cap.read()
                if not ret:
                    break

                frame_counter += 1
                if frame_counter % motion_frame_interval != 0:
                    continue

                fg_mask = bg_subtractor.apply(frame)
                motion_pixels = cv2.countNonZero(fg_mask)

                if motion_pixels > 3000:
                    out.write(frame)
                else:
                    break

                if time.time() - start_time >= videotime * 60:
                    if Updisk:
                        for disk in Networkdisk:
                            if disk == 1:
                                sync = threading.Thread(target=bysync, args=(cu_videopath, Cameraname, 0, deletevd))
                            elif disk == 2:
                                sync = threading.Thread(target=alisync, args=(cu_videopath, Cameraname, 0, deletevd))
                            sync.start()
                    video_total_size += os.path.getsize(cu_videopath)  # 更新视频总大小
                    out.release()
                    if video_total_size >= upload_threshold * (1024 * 1024 * 1024):
                        check_and_delete_earlier_videos()  # 检测网盘空间并删除早期视频
                    break

    cv2.destroyAllWindows()
    cap.release()
    out.release()

if __name__ == '__main__':
    capture(NVRurl, Cameraname, videopath, videotime, Updisk, deletevd, Networkdisk, Networkdisk_space_threshold, upload_threshold)
