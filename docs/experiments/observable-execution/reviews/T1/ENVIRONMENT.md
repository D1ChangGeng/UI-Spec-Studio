# Product review environment

Review three anonymous frozen applications in R7/app, T4/app and M2/app. The task is TASK.md. Do not edit applications. Do not inspect participant workspaces, method files, archived outward messages or the method mapping. First operate the products in a browser and write your perceptual observations; inspect source afterwards only to explain a concrete observation. The app README is an author claim, so defer it until product observations are recorded.

Node dependencies are already available through node_modules. Start each Vite server as needed using ports 8661, 8662, 8663 for R7, T4, M2 respectively. Python Playwright: /workspace/scratch/654b1ee6916f/ui-spec-preview-env/bin/python. Browser: /workspace/scratch/654b1ee6916f/ui-spec-browsers/chrome-headless-shell-linux64/chrome-headless-shell. Use FONTCONFIG_FILE=/workspace/scratch/654b1ee6916f/ui-spec-fonts/fonts.conf and PLAYWRIGHT_BROWSERS_PATH=/workspace/scratch/654b1ee6916f/ui-spec-browsers. Local browser/server commands need require_escalated because the default sandbox lacks sockets.

Save review code, measurements, actual screenshots and your review in this directory, outside app/. Distinguish capture from actually viewed evidence; do not claim natural-speed playback if only sequence frames or timing data were examined. Do not change a product after finding a gap.
