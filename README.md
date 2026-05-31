# realtime-finance
A simple application that displays currency and gold exchange rate changes on the Linux desktop screen
This application obtains exchange rate data via the "https://api.genelpara.com/" service


Clone the repository
```bash
git clone https://github.com/heyderismayilli092/realtime-finance ~/realtime-finance
```

Run application
```bash
python3 ~/realtime-finance/src/main.py
```

### Build .deb package
```bash
sudo apt install devscripts git-buildpackage
sudo mk-build-deps -ir
gbp buildpackage --git-export-dir=/tmp/build/realtime-finance -us -uc
```

### **Screenshots**

![realtime-finance 1](screenshots/realtime-finance-1.png)
![realtime-finance 2](screenshots/realtime-finance-2.png)
![realtime-finance 3](screenshots/realtime-finance-3.png)
![realtime-finance 4](screenshots/realtime-finance-4.png)
![realtime-finance 5](screenshots/realtime-finance-5.png)


NOTE: This software was prepared as part of the "Teknofest 2026 Pardus Bug Finding and Suggestion Competition"

