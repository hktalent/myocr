from PIL import Image
from PIL.ExifTags import TAGS, GPSTAGS

# 定义经纬度的tag值
LATITUDE_TAG = 0x0002
LONGITUDE_TAG = 0x0004

# 定义度分秒格式对应的tag值
LATITUDE_REF_TAG = 0x0001
LATITUDE_DMS_TAG = 0x0003
LONGITUDE_REF_TAG = 0x0003
LONGITUDE_DMS_TAG = 0x0005

# 定义需要修改的经纬度
latitude = 40.7127837  # 纬度
longitude = -74.0059413  # 经度

# 打开图片文件
# 打开图片文件
with Image.open("i1.jpg") as img:
    # 获取图片的exif信息
    exif_data = img.getexif()
    
    # 解析exif信息
    exif = {}
    if exif_data:
        for tag_id, value in exif_data.items():
            tag = TAGS.get(tag_id, tag_id)
            exif[tag] = value
    
        # 检查是否存在GPS信息
        gps_info = exif.get("GPSInfo", {})
        if gps_info:
            # 获取原始的经纬度信息
            lat = gps_info.get(LATITUDE_TAG)
            lon = gps_info.get(LONGITUDE_TAG)
            
            # 将原始的经纬度信息转换为度分秒格式
            lat_ref = gps_info.get(LATITUDE_REF_TAG)
            lon_ref = gps_info.get(LONGITUDE_REF_TAG)
            lat_dms = calculate_dms(lat)
            lon_dms = calculate_dms(lon)
            
            # 修改度分秒格式的经纬度信息
            lat_dms_new = convert_dms(latitude, True)
            lon_dms_new = convert_dms(longitude, False)
            
            # 将修改后的经纬度信息转换为原始数值格式
            lat_new = convert_to_raw(lat_dms_new)
            lon_new = convert_to_raw(lon_dms_new)
            
            # 更新exif信息
            gps_info[LATITUDE_TAG] = lat_new
            gps_info[LONGITUDE_TAG] = lon_new
            gps_info[LATITUDE_REF_TAG] = 'N' if latitude >= 0 else 'S'
            gps_info[LONGITUDE_REF_TAG] = 'E' if longitude >= 0 else 'W'
        else:
            print("No GPS information found in the image exif data!")
    
    # 保存修改后的图片文件
    img.save("example_new.jpg", exif=exif)