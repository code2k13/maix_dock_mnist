import sensor
import image
import time
import KPU as kpu

sensor.reset()
sensor.set_pixformat(sensor.GRAYSCALE)
sensor.set_framesize(sensor.QQVGA)
sensor.set_vflip(True)
sensor.set_hmirror(True)

QQVGA_WIDTH = 160
QQVGA_HEIGHT = 120

task = kpu.load(0x300000)
kpu.set_layers(task, 11)

clock = time.clock()
while True:
    clock.tick()
    img = sensor.snapshot()
    img2 = img.copy()
    img = img.invert()
    blobs = img.find_blobs([(73, 200)], pixels_threshold=50, area_threshold=50, merge=False)

    if blobs:
        tile_index = 0

        for b in blobs:

            #tmp = img.draw_rectangle(b[0:4])
            roi =  b[0:4]

            x0 = max(0,roi[0]-4)
            y0 = max(0,roi[1]-4)
            x1 = min(QQVGA_WIDTH-x0,roi[2]+8)
            y1 = min(QQVGA_HEIGHT-y0,roi[3]+8)

            f = img.copy((x0,y0,x1,y1))
            f = f.resize(28, 28)
            f.strech_char(1)
            f.pix_to_ai()
            fmap = kpu.forward(task, f)
            plist = fmap[:]
            prediction = max(range(len(plist)), key=lambda x: plist[x])

            # Draw the tile and prediction on the main image
            img2.draw_rectangle(x0,y0,x1,y1,color=0)
            img2.draw_string(x0,y0+y1, str(prediction),color=0,scale=2)

        #comment this line for more speed
        #or change to lcd.show(img2) for displaying on LCD
        print(img2.compressed_for_ide())

        fps = clock.fps()
        print("%2.1f fps" % fps)

    time.sleep_ms(200)
