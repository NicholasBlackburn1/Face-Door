import uvicorn
from vidgear.gears.asyncio import WebGear

#various performance tweaks
options = {"frame_size_reduction": 40, "frame_jpeg_quality": 80, "frame_jpeg_optimize": True, "frame_jpeg_progressive": True}

while True:
    web = WebGear(source = "output.avi", logging = True, **options)
    #run this app on Uvicorn server at address http://0.0.0.0:8000/
    uvicorn.run(web(), host='0.0.0.0', port=8000)
