import axios from 'axios'

const API_URL = process.env.REACT_API_URL || 'http://localhost:5000/api'

const api = axios.create({
    baseURL: API_URL
});

api.interceptors.request.use(config=>{
    const token = localStorage.getItem('token');
    if(token){
        config.headers.Authorization = `Bearer ${token}`;
    }
    return config
})


//--- AUTH---
export async function loginUser(email,password) {
    try{
        const response = await api.post('/auth/login',{
            email: email,
            password: password
        });
        return response.data;
    }catch(error){
        throw new Error(
            error.response?.data?.error || 'Login Failed. Please try again later'
        );
    }
}

export async function getCurrUser() {
    try{
        const response = await api.get('auth/me');
        return response.data;
    }catch (error){
        throw new Error(
            error.response?.data?.error || 'Failed to Get user information. Please try again after some time'
        );
    }
}

//--- CATEGORY---

export async function getCategory() {
    try{
        const response = await api.get('/categories');
        return response.data;
    }catch (error){
        throw new Error(
            error.response?.data?.error || 'Failed to get Categories'
        );
    }
}

export async function createCategory(data) {
    try{
        const response = await api.post('/categories',data);
        return response.data;
    }catch (error){
        throw new Error(
            error.response?.data?.error || 'Failed to create category'
        );
    }
}


export async function deleteCategory(id) {
    try{
        const response = await api.delete(`/categories/${id}`);
        return response.data;
    }catch (error){
        throw new Error(
            error.response?.data?.error || 'Failed to delete category'
        );
    }
}

//--- PRODUCTS ---
export async function getProducts(search='', categoryId = '') {
    try{
        const params = {};
        if(search) params.search = search;
        if(categoryId) params.categoryId = categoryId;

        const response = await api.get('/products',{params});
        return response.data;
    }catch (error){
        throw new Error(
            error.response?.data?.error || 'Failed to fetch products'
        );
    }
}


export async function getLowStockProducts() {
    try{
        const response = await api.get('/products/low-stock');
        return response.data;
    }catch (error){
        throw new Error(
            error.response?.data?.error || 'Failed to create category'
        );
    }
}

export async function createProducts(data) {
    try{
        const response = await api.post('/products',data);
        return response.data;
    }catch (error){
        throw new Error(
            error.response?.data?.error || 'Failed to create product'
        );
    }
}


export async function updateProducts(id,data) {
    try{
        const response = await api.put(`/products/${id}`,data);
        return response.data;
    }catch (error){
        throw new Error(
            error.response?.data?.error || 'Failed to update product information'
        );
    }
}

export async function deleteProduct(id) {
    try{
        const response = await api.delete(`/products/${id}`);
        return response.data;
    }catch (error){
        throw new Error(
            error.response?.data?.error || 'Failed to delete product'
        );
    }
}

//--- SALES ---
export async function getSales() {
    try{
        const response = await api.get('/sales');
        return response.data;
    }catch (error){
        throw new Error(
            error.response?.data?.error || 'Failed to fetch sales information'
        );
    }
}


export async function getMySales() {
    try{
        const response = await api.get('/sales/my-sales');
        return response.data;
    }catch (error){
        throw new Error(
            error.response?.data?.error || 'Failed to create category'
        );
    }
}

export async function recordSale(data) {
    try{
        const response = await api.post('/products',data);
        return response.data;
    }catch (error){
        throw new Error(
            error.response?.data?.error || 'Failed to create category'
        );
    }
}


//--- DASHBOARD ---
export async function getDashboardSummary() {
    try{
        const response = await api.get('/dashboard/summary');
        return response.data;
    }catch (error){
        throw new Error(
            error.response?.data?.error || 'Failed to create category'
        );
    }
}


export async function getRevenueByDay() {
    try{
        const response = await api.get('/dashboard/revenue-by-day');
        return response.data;
    }catch (error){
        throw new Error(
            error.response?.data?.error || 'Failed to create category'
        );
    }
}

export async function getTopProducts() {
    try{
        const response = await api.get('/dashboard/top-products');
        return response.data;
    }catch (error){
        throw new Error(
            error.response?.data?.error || 'Failed to create category'
        );
    }
}

export async function getRevenueByCategory() {
    try{
        const response = await api.get('/dashboard/revenue-by-category');
        return response.data;
    }catch (error){
        throw new Error(
            error.response?.data?.error || 'Failed to create category'
        );
    }
}