run-server:
	@echo "Kill the potential PID processes that use 5000 port"
	@kill -9 $$(lsof -t -i:5000)
	@echo "Running server..."
	@python ./backend/backend/app.py