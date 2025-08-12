# Alternative Workflow with Publish Profile
# Replace the login and deploy steps with this if federated identity keeps failing:

      - name: 'Deploy to Azure Web App'
        uses: azure/webapps-deploy@v3
        id: deploy-to-webapp
        with:
          app-name: ${{ env.AZURE_WEBAPP_NAME }}
          slot-name: 'Production'
          package: .
          publish-profile: ${{ secrets.AZUREAPPSERVICE_PUBLISHPROFILE }}

# To get the publish profile:
# 1. Go to Azure Portal → App Services → my-ai-assistant
# 2. Click "Get publish profile" 
# 3. Copy the XML content
# 4. Add it as a GitHub secret named AZUREAPPSERVICE_PUBLISHPROFILE
