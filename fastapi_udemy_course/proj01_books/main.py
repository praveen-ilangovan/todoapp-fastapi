"""
Main entrypoint
"""

# Project specific imports
import uvicorn

def main():
    """Main function"""
    uvicorn.run("fastapi_udemy_course.proj01_books.app:app", host="127.0.0.1", port=8000, reload=True)

if __name__ == "__main__":
    main()
