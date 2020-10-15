from travel import create_app

# want to run flask in VS Studio code, then add these lines that check if this file is being executed
if __name__=='__main__':
    n_app=create_app()
    n_app.run()