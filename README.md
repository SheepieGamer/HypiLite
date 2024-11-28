# HypiLite

A simplified and user-friendly REST API wrapper for the Hypixel API. HypiLite makes it easier to access Hypixel player data and statistics with a clean, modern API interface.

## Features

- 🚀 Simplified endpoints for common Hypixel data requests
- 📚 Comprehensive API documentation with Swagger UI
- 🔑 Secure API key handling
- ⚡ Fast response times with async operations
- 🔄 CORS enabled for web applications

## Getting Started

### Prerequisites

- Python 3.8 or higher
- Hypixel API key ([Get one here](https://developer.hypixel.net/))

### Installation

1. Clone the repository:
```bash
git clone https://github.com/SheepieGamer/hypilite.git
cd hypilite
```

2. Create and activate a virtual environment:
```bash
python -m venv .venv
# On Windows
.venv\Scripts\activate
# On Unix or MacOS
source .venv/bin/activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

### Running the API

Start the development server:
```bash
uvicorn app:app --reload
```

The API will be available at `http://localhost:8000`

## API Documentation

Once the server is running, you can access:
- Interactive API documentation (Swagger UI): `http://localhost:8000/docs`
- Alternative documentation (ReDoc): `http://localhost:8000/redoc`

## Available Endpoints

- `GET /health` - Check API health status
- `GET /` - API information and documentation links
- `GET /api/profile/{username}?key={api_key}` - Get player profile data
- More endpoints coming soon!

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Acknowledgments

- [Hypixel API](https://api.hypixel.net/) for providing the base API
- [FastAPI](https://fastapi.tiangolo.com/) for the excellent web framework
