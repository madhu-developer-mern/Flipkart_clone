# ECommerce Application - Real-time Shopping Platform

A full-stack e-commerce application similar to Flipkart built with Python FastAPI backend and React frontend. 

## Features

### Backend (FastAPI)
- 🚀 Real-time product search from Flipkart
- 📦 Web scraping with BeautifulSoup
- ⚡ Fast async API endpoints
- 🎯 Product filtering and sorting
- 💾 In-memory caching
- 🔄 CORS enabled for frontend access
- 📊 Mock product data fallback

### Frontend (React)
- 🎨 Modern, responsive UI similar to Flipkart
- 🔍 Real-time product search
- 📱 Mobile-friendly design
- 🛒 Shopping cart interface
- ❤️ Wishlist functionality
- ⭐ Product ratings and reviews
- 💰 Price filtering and sorting
- 🏷️ Category browsing
- 📸 Product image gallery
- 📋 Product details modal

## Project Structure

```
ecommerce2/
├── backend/
│   ├── main.py              # FastAPI application
│   ├── requirements.txt      # Python dependencies
│   └── .gitignore
├── frontend/
│   ├── public/
│   │   └── index.html       # HTML entry point
│   ├── src/
│   │   ├── components/
│   │   │   ├── Navbar.js
│   │   │   ├── Categories.js
│   │   │   ├── ProductList.js
│   │   │   └── ProductModal.js
│   │   ├── App.js           # Main App component
│   │   ├── App.css          # App styles
│   │   ├── index.js         # React entry point
│   │   └── index.css        # Global styles
│   ├── package.json         # Node dependencies
│   └── .gitignore
└── README.md
```

## Installation & Setup

### Prerequisites
- Node.js (v14+)
- Python 3.8+
- npm or yarn

### Backend Setup

1. Navigate to the backend directory:
```bash
cd backend
```

2. Create a Python virtual environment:
```bash
# Windows
python -m venv venv
venv\Scripts\activate

# macOS/Linux
python3 -m venv venv
source venv/bin/activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Run the FastAPI server:
```bash
python main.py
```

The backend will start at `http://localhost:8000`

### Frontend Setup

1. Navigate to the frontend directory:
```bash
cd frontend
```

2. Install dependencies:
```bash
npm install
```

3. Start the development server:
```bash
npm start
```

The frontend will open at `http://localhost:3000`

## API Endpoints

### GET `/`
- Returns welcome message and API version

### GET `/api/search`
- Search for products
- **Parameters:**
  - `q` (string): Search query (required, minimum 2 characters)
  - `limit` (integer): Maximum products to return (optional, default: 20, max: 100)
- **Response:** List of products with details

### GET `/api/categories`
- Get all available categories
- **Response:** List of categories with icons

### GET `/api/trending`
- Get trending products
- **Response:** List of top 6 trending products

### GET `/health`
- Health check endpoint
- **Response:** Server status

## Usage

1. **Search Products**: Type in the search bar to find products
2. **Filter by Category**: Click on category cards to browse products
3. **Sort Results**: Use sorting options (Price, Rating, Relevance)
4. **Filter by Price**: Use the price range slider in the sidebar
5. **View Details**: Click on any product to see full details in a modal
6. **Add to Cart**: Click "Add to Cart" button (UI implemented)
7. **Add to Wishlist**: Click heart icon to save products

## Web Scraping

The application scrapes product information from Flipkart including:
- Product names
- Prices
- Product images
- Ratings
- Review counts

**Note:** Web scraping may fail due to Flipkart's anti-scraping measures. The app includes mock data fallback to ensure functionality.

## API Response Format

```json
{
  "query": "electronics",
  "products": [
    {
      "id": "12345",
      "name": "Samsung Galaxy M31",
      "price": "₹9,999",
      "image_url": "https://...",
      "rating": "4.5",
      "reviews": "15.2K"
    }
  ],
  "cached": false,
  "count": 20
}
```

## Caching

The backend implements in-memory caching to improve performance:
- Search results are cached with key format: `{query}_{limit}`
- Cache persists during the server session
- Very useful for frequently searched queries

## Dependencies

### Backend
- FastAPI
- Uvicorn
- Requests
- BeautifulSoup4
- Pydantic
- lxml

### Frontend
- React
- Axios
- CSS3

## Browser Support

- Chrome (latest)
- Firefox (latest)
- Safari (latest)
- Edge (latest)
- Mobile browsers (iOS Safari, Chrome Mobile)

## Performance

- **Backend Response Time**: ~200-500ms for searches
- **Page Load**: ~1-2 seconds
- **Image Loading**: Optimized with lazy loading
- **Caching**: Instant response for cached queries

## Security Considerations

- CORS enabled for development (should be restricted in production)
- Input validation on all API endpoints
- Rate limiting recommended for production
- HTTPS recommended for production deployment

## Future Enhancements

- [ ] User authentication & authorization
- [ ] Real database (PostgreSQL/MongoDB)
- [ ] Shopping cart persistence
- [ ] Payment gateway integration
- [ ] Order management
- [ ] Admin dashboard
- [ ] Advanced filtering (brand, color, size)
- [ ] Product reviews & ratings system
- [ ] User wishlist persistence
- [ ] Real-time inventory updates
- [ ] Email notifications
- [ ] Mobile app (React Native)

## Troubleshooting

### Backend Issues

**Problem:** `ModuleNotFoundError: No module named 'fastapi'`
- Solution: Make sure to activate the virtual environment and install requirements

**Problem:** Port 8000 already in use
- Solution: Change port in main.py: `uvicorn.run(app, host="0.0.0.0", port=8001)`

**Problem:** CORS errors
- Solution: Frontend URL may not match. Check localhost vs 127.0.0.1

### Frontend Issues

**Problem:** `npm install` fails
- Solution: Clear npm cache: `npm cache clean --force`

**Problem:** API calls failing
- Solution: Check if backend is running on `http://localhost:8000`

**Problem:** Blank page on startup
- Solution: Check browser console for errors, ensure Node version is 14+

## Development Mode

To develop locally:

1. Keep backend running in one terminal
2. Keep frontend running in another terminal
3. Make changes and see them live with hot reloading
4. Check browser console for frontend errors
5. Check terminal for backend errors

## Production Deployment

### Backend
```bash
# Build
pip install -r requirements.txt

# Run with gunicorn
gunicorn -w 4 -b 0.0.0.0:8000 main:app
```

### Frontend
```bash
# Build
npm run build

# The 'build' folder is ready to be deployed
```

## License

MIT License - Feel free to use this project for learning and development

## Support

For issues or questions, check:
- FastAPI Documentation: https://fastapi.tiangolo.com/
- React Documentation: https://react.dev/
- BeautifulSoup Documentation: https://www.crummy.com/software/BeautifulSoup/

---

**Built with ❤️ for e-commerce enthusiasts**

Last Updated: February 22, 2026
