        parsed_data = json.loads(message)
        success = parsed_data.get("login")
        if success is True: