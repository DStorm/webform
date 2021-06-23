#!/bin/bash
echo "Pulling from prod..."
git pull origin prod
echo "Successfully pulled from prod!"
echo "Restarting server..."
echo "Restarting webform.service..."
sudo systemctl restart webform
echo "Successfully restarted webform!"
echo "Restarting nginx.service..."
sudo systemctl restart nginx
echo "Successfully restarted nginx!"
