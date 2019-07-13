from app import app
import base64
if __name__ == '__main__':
    app.debug = app.config['DEBUG'] # 配置为Debug模式，这样修改文件后，会自动重启服务
    app.run() # 这里配置为可在局域网中访问，默认为127.0.0.1，只能在本机访问
