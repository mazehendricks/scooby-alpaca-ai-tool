// Main JavaScript File
document.addEventListener('DOMContentLoaded', () => {
    console.log('Page loaded successfully');
    
    // Example: Fetch data from an API
    async function fetchData(url) {
        try {
            const response = await fetch(url);
            const data = await response.json();
            console.log('Fetched data:', data);
            return data;
        } catch (error) {
            console.error('Error fetching data:', error);
        }
    }
    
    // Usage examples:
    // fetchData('https://api.example.com/data');
    // fetchData('https://jsonplaceholder.typicode.com/posts');
});
