# Model Deployment Automation

This repository contains a GitHub Actions workflow that automatically calls your model registration/update APIs whenever a model becomes available.

## 🚀 Features

- **Automatic Registration**: Registers the `mlt-batch` model when triggered by code changes
- **Manual Updates**: Manually trigger registration or updates via GitHub UI
- **Hardcoded Configuration**: Uses your exact API endpoints and model metadata
- **Real API Integration**: Calls your actual Postman APIs
- **Comprehensive Logging**: Detailed output for debugging and monitoring

## 📁 Repository Structure

```
├── .github/
│   └── workflows/
│       └── model-deployment.yml    # GitHub Actions workflow (currently blocked by IP restrictions)
├── model-configs/                  # Example configuration files (for reference)
├── scripts/
│   └── model_deployment.py        # Original deployment script (for testing)
├── manual-model-register.py       # ✅ WORKING: Manual registration from local machine
├── test-local-api.py              # API testing and debugging script
├── test_env/                      # Python virtual environment (for local testing)
└── README.md                      # This documentation
```

## 🛠️ Setup Instructions

### 1. ⚠️ IP Restriction Issue Identified

**Current Status**: API works locally but **GitHub Actions is blocked** due to IP restrictions.

- **API URL**: `https://backoffice.dev.api.discomax.com/mlp-metadata-manager/meta-manager`
- **Authentication**: None required ✅
- **Problem**: GitHub Actions runners get `403 Forbidden`
- **Cause**: API only allows specific IP ranges/networks

**Solutions Available**:
- ✅ **Manual script**: Use `manual-model-register.py` from your machine
- 🔧 **Self-hosted runner**: Set up runner on your network  
- 📞 **Team coordination**: Ask team to whitelist GitHub Actions IPs

### 2. Hardcoded Model Configuration

The workflow is currently configured for the `mlt-batch` model with these hardcoded settings:

```json
{
  "model_name": "mlt-batch",
  "variant": "sllim-tg-pkg-300",
  "owner_team": "personalization",
  "omd_business_service": "content-discovery"
}
```

To modify the model information, edit the workflow file directly: `.github/workflows/model-deployment.yml`

### 3. Workflow Triggers

The workflow triggers on:

1. **Push to main**: When any changes are pushed to the main branch (simulating model availability)
2. **Manual trigger**: Via GitHub Actions UI for testing

## 🔧 Usage

### ⚠️ Current Status: GitHub Actions Blocked

**GitHub Actions workflow is currently non-functional** due to IP restrictions. Use these alternatives:

### ✅ Solution 1: Manual Script (Works Now)

Use the manual script from your local machine:

```bash
# In virtual environment
source test_env/bin/activate
python manual-model-register.py
```

**Choose from menu:**
- Register new model (creates unique variant)
- Update existing model configuration

### 🔧 Solution 2: Self-Hosted Runner (Advanced)

1. Set up a self-hosted GitHub Actions runner on your network
2. In the workflow file, change:
   ```yaml
   runs-on: self-hosted  # Instead of ubuntu-latest
   ```
3. GitHub Actions will run on your network (has API access)

### 📞 Solution 3: Team Coordination (Long-term)

Ask your team to:
- Whitelist GitHub Actions IP ranges in API firewall
- Or provide API credentials for external access

### Testing the API Connection

You can test the API connection directly with curl (no authentication needed):

```bash
# Test the API directly
curl -X POST "https://backoffice.dev.api.discomax.com/mlp-metadata-manager/meta-manager/v1/models/register" \
     -H "Content-Type: application/json" \
     -d '{"model_name": "test", "variant": "v1.0.0"}'
```

## 📊 API Endpoints

The workflow calls these actual API endpoints:

### Register Model
- **Full URL**: `https://backoffice.dev.api.discomax.com/mlp-metadata-manager/meta-manager/v1/models/register`
- **Method**: `POST`
- **Payload**: Complete model configuration (hardcoded in workflow)

### Update Model  
- **Full URL**: `https://backoffice.dev.api.discomax.com/mlp-metadata-manager/meta-manager/v1/models/update/CD:personalization:mlt-batch:sllim-tg-pkg-3`
- **Method**: `PUT`
- **Payload**: 
```json
{
  "model": {
    "serving_configuration": {
      // Only serving configuration fields
    }
  }
}
```

## 🔍 Monitoring and Logs

### Viewing Workflow Logs

1. Go to `Actions` tab in your repository
2. Click on the workflow run
3. Expand job steps to view detailed logs

### Log Output Examples

**Successful Registration**:
```
🚀 Registering model: mlt-batch (variant: sllim-tg-pkg-300)
📡 API URL: https://api.example.com/v1/models/register
✅ Model registered successfully!
📄 Response: {"status": "success", "model_id": "..."}
```

**Successful Update**:
```
🔄 Updating model: CD:personalization:mlt-batch:sllim-tg-pkg-3
📡 API URL: https://api.example.com/v1/models/update/CD:personalization:mlt-batch:sllim-tg-pkg-3
✅ Model updated successfully!
```

## 🚨 Troubleshooting

### ⚠️ Known Issue: 403 Forbidden in GitHub Actions

**Root Cause**: API has IP restrictions - allows local/internal networks but blocks GitHub's cloud runners.

**Status**: 
- ✅ **Local machine**: Works perfectly (Status 200/201)
- ❌ **GitHub Actions**: 403 Forbidden (IP blocked)

**Solution**: Use the `manual-model-register.py` script or set up self-hosted runner.

### Other Common Issues

1. **Model Already Exists Error**
   - This is normal! Scripts handle "already exists" gracefully
   - Each registration uses a unique timestamp variant to avoid conflicts

2. **Model Not Found (Update)**
   - Ensure model was previously registered
   - The hardcoded model ID is: `CD:personalization:mlt-batch:sllim-tg-pkg-3`

3. **Requests Module Not Found** (Local script)
   - Create virtual environment: `python3 -m venv test_env`
   - Activate it: `source test_env/bin/activate`
   - Install requests: `pip install requests`

### Debugging Steps

1. **Check workflow logs** in GitHub Actions tab
2. **Test API connectivity** manually using curl:
   ```bash
   curl -X POST "https://backoffice.dev.api.discomax.com/mlp-metadata-manager/meta-manager/v1/models/register" \
        -H "Content-Type: application/json" \
        -d '{"model_name": "test", "variant": "debug-test"}'
   ```
3. **Check network connectivity** to the API endpoint
4. **Review API response** for detailed error messages

## 🔒 Security Considerations

- No authentication required for the API (public development endpoint)
- Workflow runs on main branch pushes (consider branch protection rules)
- API endpoint is hardcoded in workflow (review before committing)  
- Be cautious when registering models in development environment

## 🛡️ Best Practices

1. **Testing**: Test the workflow manually before relying on automatic triggers
2. **Monitoring**: Set up alerts for workflow failures in GitHub Actions
3. **Version Control**: Document model changes in commit messages
4. **Access Control**: Limit repository access to authorized team members
5. **Environment Awareness**: Remember this connects to a development API endpoint

## 📝 Example Usage

Here's how to use the workflow:

### Automatic Registration (when model becomes available)
```bash
# 1. Make any change to trigger the workflow
echo "Model v1.0.0 is ready" > model-ready.txt

# 2. Commit and push to main
git add model-ready.txt
git commit -m "Model mlt-batch sllim-tg-pkg-300 is available"
git push origin main

# 3. Workflow automatically triggers and registers the hardcoded model
# Check the Actions tab to see the results
```

### Manual Testing
```bash
# 1. Go to GitHub Actions tab
# 2. Select "Model Deployment Automation" workflow  
# 3. Click "Run workflow"
# 4. Choose "register" or "update"
# 5. Click "Run workflow" button
```

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test using dry-run mode
5. Submit a pull request

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.