## cURL
1. Test connection (GET)
   ```sh
   curl --location 'http://127.0.0.1:5000'
   ```
2. Predict (POST)
   ```sh
   curl --location 'http://127.0.0.1:5000/predict' \
   --header 'Content-Type: application/json' \
   --data '{
     "n": "130",
     "p": "300",
     "k": "220",
     "ph": "8.929663",
     "lat": "-5.389754211186734",
     "lon": "104.70190313407653"
   }
   ```

## Deployment on GCE
1. Create new firewall rule with the following configuration:
   - Name: <strong>allow-app</strong>
   - Direction: ingress
   - Target tags: `<target-vm>` (If a firewall rule with the same configuration already exists, just add the new target VM to the target tags)
   - IP ranges: 0.0.0.0/0
   - Protocols and ports:
     - TCP: 8080
2. Create new instance with the following configuration:
   - Name: `<vm-name>`
   - Region: `<region>`
   - Machine type: e2-medium
   - Image: Debian, Debian GNU/Linux, 12 (bookworm), amd64 built on 20240910
   - Network interface:
     - External IPv4 address: click "RESERVE STATIC EXTERNAL IP ADDRESS" and then give it a name. Click "Reserve."
   - Network Tags: `<target-vm>`
3. SSH to the VM
4. Update and Install Required Packages:
   ```sh
   sudo apt update
   sudo apt upgrade -y
   sudo apt install python3-pip python3-venv -y
   ```
5. Upload main.py, requirements.txt, data.json and model10plantrec.h5 to VM
6. Create a virtual environment and activate it:
   ```sh
   python3 -m venv myenv
   source myenv/bin/activate
   ```
7. Install the required Python packages listed in your requirements.txt file:
   ```sh
   pip install -r requirements.txt
   ```
8. Run and test your Flask app:
   ```sh
   python main.py
   ```
   Your flask app should now be accessible via your static external IP on port 8080:
   ```sh
   http://<your_static_ip>:8080
   ```

The above configuration will stop if the VM shuts down, either intentionally or accidentally. You need to restart it manually. To ensure the application runs automatically on VM startup, follow these steps:
1. Create a systemd service file:
   ```sh
   sudo nano /etc/systemd/system/flaskapp.service
   ```
2. Add the following content to the file:
   ```sh
   [Unit]
   Description=Gunicorn instance to serve flask app
   After=network.target

   [Service]
   User=your_user
   Group=www-data
   WorkingDirectory=/home/your_user/
   Environment="PATH=/home/your_user/myenv/bin"
   ExecStart=/home/your_user/myenv/bin/python main.py

   [Install]
   WantedBy=multi-user.target
   ```
   Replace `your_user` with your username.
3. Reload systemd and start your service:
   ```sh
   sudo systemctl daemon-reload
   sudo systemctl start flaskapp
   sudo systemctl enable flaskapp
   ```

   
