#!/bin/bash
# Hamada Tool V2 - Quick Setup Script

echo "🏢 Setting up Hamada Tool V2 for AEDCO..."
echo "=========================================="

# Create virtual environment
echo "📦 Creating virtual environment..."
python3 -m venv hamada-env
source hamada-env/bin/activate || hamada-env\Scripts\activate

# Install dependencies
echo "⬇️ Installing dependencies..."
pip install --upgrade pip
pip install -r requirements.txt

# Create environment file
echo "⚙️ Setting up environment..."
if [ ! -f .env ]; then
    cp .env.example .env
    echo "✅ Created .env file - please configure your settings"
else
    echo "⚠️ .env file already exists"
fi

# Create data directories
echo "📁 Creating data directories..."
mkdir -p data/uploads data/templates data/exports
mkdir -p logs

echo ""
echo "✅ SETUP COMPLETE!"
echo "=================="
echo ""
echo "🚀 To start the application:"
echo "1. Activate virtual environment: source hamada-env/bin/activate"
echo "2. Run the application: streamlit run main.py"
echo "3. Open your browser: http://localhost:8501"
echo "4. Login with: admin / admin123"
echo ""
echo "🏢 Hamada Tool V2 is ready for AEDCO!"
echo "📞 Support: +20100 0266 344"
