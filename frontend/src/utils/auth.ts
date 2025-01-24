import axios from 'axios';
import config from '../config';

interface TokenResponse {
  access: string;
  refresh: string;
}

class AuthService {
  private static instance: AuthService;
  private accessToken: string | null = null;
  private refreshToken: string | null = null;

  private constructor() {
    // Load tokens from localStorage if they exist
    this.accessToken = localStorage.getItem('accessToken');
    this.refreshToken = localStorage.getItem('refreshToken');
  }

  public static getInstance(): AuthService {
    if (!AuthService.instance) {
      AuthService.instance = new AuthService();
    }
    return AuthService.instance;
  }

  public async initialize(): Promise<void> {
    if (!this.accessToken) {
      await this.getNewTokens();
    }
  }

  public getAccessToken(): string | null {
    return this.accessToken;
  }

  private async getNewTokens(): Promise<void> {
    try {
      const response = await axios.post<TokenResponse>(
        `${config.apiBaseUrl}/api/token/`,
        {},
        {
          headers: {
            'X-API-Key': config.apiKey,
            'Content-Type': 'application/json',
          },
        }
      );

      this.setTokens(response.data.access, response.data.refresh);
    } catch (error) {
      console.error('Failed to get tokens:', error);
      throw error;
    }
  }

  private async refreshAccessToken(): Promise<void> {
    if (!this.refreshToken) {
      await this.getNewTokens();
      return;
    }

    try {
      const response = await axios.post<TokenResponse>(
        `${config.apiBaseUrl}/api/token/refresh/`,
        {
          refresh: this.refreshToken,
        }
      );

      this.setTokens(response.data.access, response.data.refresh);
    } catch (error) {
      console.error('Failed to refresh token:', error);
      // If refresh fails, try getting new tokens
      await this.getNewTokens();
    }
  }

  private setTokens(accessToken: string, refreshToken: string): void {
    this.accessToken = accessToken;
    this.refreshToken = refreshToken;
    localStorage.setItem('accessToken', accessToken);
    localStorage.setItem('refreshToken', refreshToken);
  }

  public async handleTokenRefresh(): Promise<string> {
    await this.refreshAccessToken();
    return this.accessToken!;
  }
}

export default AuthService;
