# Deployment Guide - HF Spaces

## 📋 Deployment Checklist

### ✅ Pre-Deployment Verification

1. **API Endpoints** (all return 200):
   ```bash
   # Test reset
   curl -X POST http://localhost:8000/reset
   
   # Test step
   curl -X POST http://localhost:8000/step \
     -H "Content-Type: application/json" \
     -d '{"action": "buy"}'
   
   # Test close
   curl -X POST http://localhost:8000/close
   ```

2. **Inference Output Format**:
   ```bash
   python inference.py
   ```
   Expected: `[START]`, `[STEP]`, `[END]`, `[SUMMARY]` format ✅

3. **Docker Build**:
   ```bash
   docker build -t trading-env .
   docker run -p 7860:7860 trading-env
   ```

4. **OpenEnv Configuration**:
   - `openenv.yaml` exists and is valid
   - All graders return scores in [0, 1]
   - 3+ tasks defined (easy, medium, hard)

### 🚀 Deploy to HF Spaces

1. **Create Space**:
   - Go to https://huggingface.co/spaces/new
   - Name: `trading-env`
   - License: Apache-2.0
   - Space SDK: Docker

2. **Push Repository**:
   ```bash
   git clone https://huggingface.co/spaces/YOUR_USER/trading-env
   cd trading-env
   
   # Copy all files from local project
   cp -r ../OPEN-ENV/* .
   
   git add .
   git commit -m "Initial commit: trading environment"
   git push
   ```

3. **Wait for Build**:
   - Docker build will start automatically
   - Should complete in < 5 minutes
   - Check Space logs if issues

4. **Verify Space is Live**:
   ```bash
   curl -X POST https://YOUR_USER-trading-env.hf.space/reset
   ```
   Should return 200 with state data

### ✅ Validator Checks

When validator runs, it checks:

1. ✅ **API Endpoint** - `/reset` returns 200
2. ✅ **Step Execution** - `/step` changes state and returns reward
3. ✅ **Close** - `/close` ends episode gracefully
4. ✅ **OpenEnv Spec** - Valid YAML, all tasks registered
5. ✅ **Graders** - All produce scores in [0, 1]
6. ✅ **Inference** - Output matches strict format
7. ✅ **Dockerfile** - Builds successfully in < 10 min

### 🔍 Troubleshooting

**Issue: /reset returns 404**
- Check `server/app.py` exists and has `@app.post("/reset")`
- Verify import: `from server.app import app`

**Issue: Graders fail validation**
- Ensure all graders return `{"score": float, ...}`
- Score must be in [0, 1] range
- Use `round(score, 3)` for precision

**Issue: Inference output format wrong**
- Must follow: `[START] task=X env=openenv model=inference`
- Must have: `[STEP] step=N action=X reward=X done=X error=X`
- Must end: `[END] success=X steps=N score=X rewards=X,X,...`
- No extra output before/after

**Issue: Docker build fails**
- Check `Dockerfile` syntax
- Verify `pyproject.toml` has correct dependencies
- Test locally: `docker build -t test .`

### 📊 Score Interpretation

Based on validator results:

| Score | Meaning |
|-------|---------|
| 0.90-1.0 | ✅ Perfect - All tests pass |
| 0.70-0.89 | ✅ Good - Minor issues fixed |
| 0.50-0.69 | ⚠️ Fair - Needs improvements |
| < 0.50 | ❌ Needs redesign |

### 📈 Optimization Tips

1. **Improve Grading**: Make graders reward profitable trades more
2. **Better Signals**: Adjust price history to have clearer trends
3. **Task Variety**: Ensure tasks are progressively harder
4. **Documentation**: Update README with strategy explanation

### 🎯 Final Submission

Once Space is live and validator passes:

1. Copy Space URL
2. Submit to evaluation
3. Monitor validation logs
4. Fix any issues reported
5. Resubmit if needed

**Space URL Format**:
```
https://{username}-trading-env.hf.space
```

**Validation Command** (when available):
```bash
./validate-submission.sh https://your-user-trading-env.hf.space
```

---

## Local Testing (Before HF Spaces)

### Test All Components

```bash
# 1. Install dependencies
pip install -e .

# 2. Start server
uvicorn server.app:app --host 0.0.0.0 --port 8000 &

# 3. Run inference
python inference.py

# 4. Test Docker
docker build -t trading-env .
docker run -p 7860:7860 trading-env

# 5. In another terminal, test Space container
curl -X POST http://localhost:7860/reset
```

### Expected Test Results

✅ All API endpoints return 200
✅ Inference runs all 3 tasks
✅ Graders produce scores in [0, 1]
✅ Docker builds in < 2 minutes
✅ Container serves API on 7860

---

**Status**: Ready for HF Spaces deployment 🚀
