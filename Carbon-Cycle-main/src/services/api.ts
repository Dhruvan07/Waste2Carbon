/**
 * CarbonCycle Centralized API Client & Endpoint Configuration
 *
 * Environment Variable:
 * - VITE_API_URL: Root host URL of the backend service (e.g. https://carbon-cycle-api.onrender.com)
 *   WITHOUT the trailing '/api' or trailing slash.
 * - In production mode, defaults to https://carbon-cycle-api.onrender.com
 * - In development mode, defaults to http://localhost:5000
 */

// 1. Resolve raw URL from Vite environment variable with smart fallback
const rawEnvUrl = (import.meta.env.VITE_API_URL as string | undefined) || '';

// Clean surrounding quotes and spaces that users often enter in dashboard env managers
const sanitizedEnvUrl = rawEnvUrl.trim().replace(/^["']|["']$/g, '').trim();

// Production fallback is the verified Render backend service URL
const DEFAULT_PROD_API = 'https://carbon-cycle-api.onrender.com';
const DEFAULT_DEV_API = 'http://localhost:5000';

const effectiveUrl = sanitizedEnvUrl || (import.meta.env.PROD ? DEFAULT_PROD_API : DEFAULT_DEV_API);

// Detect if an unreplaced placeholder or malformed URL is present
export const isInvalidUrl =
  effectiveUrl.includes('<') ||
  effectiveUrl.includes('>') ||
  !effectiveUrl.startsWith('http');

if (isInvalidUrl) {
  console.warn(
    `[CarbonCycle API Warning]: VITE_API_URL is invalid ("${effectiveUrl}"). ` +
    `Using verified production backend: ${DEFAULT_PROD_API}`
  );
}

// 2. Normalize: strip trailing slashes and any trailing '/api' to prevent double '/api/api'
const finalUrl = isInvalidUrl
  ? (import.meta.env.PROD ? DEFAULT_PROD_API : DEFAULT_DEV_API)
  : effectiveUrl;

export const API_URL = finalUrl.replace(/\/+$/, '').replace(/\/api$/, '');

// 3. Base API prefix path
export const API_BASE_URL = `${API_URL}/api`;

// 4. Strongly typed API Endpoints Map
export const API_ENDPOINTS = {
  HEALTH: `${API_URL}/api/health`,
  AUTH_REGISTER: `${API_URL}/api/auth/register`,
  AUTH_LOGIN: `${API_URL}/api/auth/login`,
  AUTH_ME: `${API_URL}/api/auth/me`,
  AUTH_LOGOUT: `${API_URL}/api/auth/logout`,
  ADMIN_USERS: `${API_URL}/api/admin/users`,
  ADMIN_DASHBOARD: `${API_URL}/api/admin/dashboard`,
} as const;

export interface HealthResponse {
  success: boolean;
  message: string;
  timestamp?: string;
}

/**
 * GET /api/health
 * Verifies backend connectivity and server status
 */
export async function checkHealthApi(): Promise<HealthResponse> {
  try {
    const res = await fetch(API_ENDPOINTS.HEALTH);
    const data = await res.json();
    return data;
  } catch (err: any) {
    console.warn('[API Health Check Warning]: Could not reach backend at', API_ENDPOINTS.HEALTH, err);
    return {
      success: false,
      message: err.message || 'Failed to reach backend health endpoint',
    };
  }
}
