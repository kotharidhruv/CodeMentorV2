pip install -r back-end/requirements.txt
cd front-end
npm install
npm run build
cp -r build ../back-end/flask_project/