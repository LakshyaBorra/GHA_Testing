# Model Deployment Automation

This repository contains a GitHub Actions workflow that automatically calls your model registration/update APIs whenever a model becomes available.

## 🚀 Features

- **Automatic Registration**: Registers the `mlt-batch` model when triggered by code changes
- **Manual Updates**: Manually trigger registration or updates via GitHub UI
- **Hardcoded Configuration**: Uses your exact API endpoints and model metadata
- **Real API Integration**: Calls your actual Postman APIs
- **Comprehensive Logging**: Detailed output for debugging and monitoring

## Testing the API Connection

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
