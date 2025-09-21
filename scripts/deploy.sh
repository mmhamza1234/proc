#!/bin/bash
# Hamada Tool V2 - Production Deployment Script

echo "🚀 Deploying Hamada Tool V2 to Production..."
echo "============================================"

# Check if running as root/admin
if [[ $EUID -eq 0 ]]; then
   echo "⚠️ Don't run as root for security reasons"
   exit 1
fi

# Create production directories
echo "📁 Creating production directories..."
sudo mkdir -p /opt/hamada-tool-v2
sudo mkdir -p /var/log/hamada-tool-v2
sudo mkdir -p /etc/hamada-tool-v2

# Copy application files
echo "📋 Copying application files..."
sudo cp -r . /opt/hamada-tool-v2/
sudo chown -R $USER:$USER /opt/hamada-tool-v2

# Install system dependencies
echo "📦 Installing system dependencies..."
sudo apt update
sudo apt install -y python3 python3-pip python3-venv nginx

# Create production virtual environment
echo "🐍 Creating production Python environment..."
cd /opt/hamada-tool-v2
python3 -m venv prod-env
source prod-env/bin/activate
pip install --upgrade pip
pip install -r requirements.txt

# Create systemd service
echo "⚙️ Creating systemd service..."
sudo tee /etc/systemd/system/hamada-tool.service > /dev/null <<EOF
[Unit]
Description=Hamada Tool V2 - AEDCO Procurement System
After=network.target

[Service]
Type=simple
User=$USER
WorkingDirectory=/opt/hamada-tool-v2
Environment=PATH=/opt/hamada-tool-v2/prod-env/bin
ExecStart=/opt/hamada-tool-v2/prod-env/bin/streamlit run main.py --server.port 8501 --server.address 127.0.0.1
Restart=always
RestartSec=10

[Install]
WantedBy=multi-user.target
EOF

# Configure nginx reverse proxy
echo "🌐 Configuring nginx..."
sudo tee /etc/nginx/sites-available/hamada-tool > /dev/null <<EOF
server {
    listen 80;
    server_name localhost;

    location / {
        proxy_pass http://127.0.0.1:8501;
        proxy_http_version 1.1;
        proxy_set_header Upgrade \$http_upgrade;
        proxy_set_header Connection "upgrade";
        proxy_set_header Host \$host;
        proxy_set_header X-Real-IP \$remote_addr;
        proxy_set_header X-Forwarded-For \$proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto \$scheme;
        proxy_cache_bypass \$http_upgrade;
    }
}
EOF

# Enable nginx site
sudo ln -sf /etc/nginx/sites-available/hamada-tool /etc/nginx/sites-enabled/
sudo nginx -t
sudo systemctl reload nginx

# Start services
echo "🔄 Starting services..."
sudo systemctl daemon-reload
sudo systemctl enable hamada-tool
sudo systemctl start hamada-tool

echo ""
echo "✅ DEPLOYMENT COMPLETE!"
echo "======================="
echo ""
echo "🌐 Application URL: http://$(hostname -I | awk '{print $1}')"
echo "📊 Service Status: sudo systemctl status hamada-tool"
echo "📋 View Logs: sudo journalctl -u hamada-tool -f"
echo "🔄 Restart Service: sudo systemctl restart hamada-tool"
echo ""
echo "🏢 Hamada Tool V2 is now running in production!"
echo "📞 AEDCO Support: +20100 0266 344"
