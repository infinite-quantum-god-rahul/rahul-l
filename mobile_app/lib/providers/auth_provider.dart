import 'package:flutter/material.dart';
import 'package:shared_preferences/shared_preferences.dart';
import 'package:flutter_secure_storage/flutter_secure_storage.dart';
import 'package:local_auth/local_auth.dart';
import '../config/app_config.dart';
import '../models/user_model.dart';
import '../services/api_service.dart';
import '../utils/constants.dart';

class AuthProvider extends ChangeNotifier {
  final ApiService _apiService = ApiService();
  final FlutterSecureStorage _secureStorage = const FlutterSecureStorage();
  final LocalAuthentication _localAuth = LocalAuthentication();
  
  User? _currentUser;
  String? _authToken;
  String? _refreshToken;
  bool _isLoading = false;
  bool _isAuthenticated = false;
  bool _isBiometricEnabled = false;
  String? _errorMessage;
  
  // Getters
  User? get currentUser => _currentUser;
  String? get authToken => _authToken;
  String? get refreshToken => _refreshToken;
  bool get isLoading => _isLoading;
  bool get isAuthenticated => _isAuthenticated;
  bool get isBiometricEnabled => _isBiometricEnabled;
  String? get errorMessage => _errorMessage;
  
  // Initialize authentication state
  Future<void> initialize() async {
    try {
      _setLoading(true);
      
      // Check for stored tokens
      await _loadStoredTokens();
      
      // Check if user is authenticated
      if (_authToken != null) {
        await _validateToken();
      }
      
      // Check biometric status
      await _checkBiometricStatus();
      
    } catch (e) {
      _setError('Failed to initialize authentication: $e');
    } finally {
      _setLoading(false);
    }
  }
  
  // Load stored tokens from secure storage
  Future<void> _loadStoredTokens() async {
    try {
      _authToken = await _secureStorage.read(key: AppConfig.authTokenKey);
      _refreshToken = await _secureStorage.read(key: AppConfig.refreshTokenKey);
      
      if (_authToken != null) {
        _isAuthenticated = true;
      }
    } catch (e) {
      _setError('Failed to load stored tokens: $e');
    }
  }
  
  // Validate stored token with server
  Future<void> _validateToken() async {
    try {
      if (_authToken == null) return;
      
      final response = await _apiService.validateToken(_authToken!);
      
      if (response['valid'] == true) {
        _currentUser = User.fromJson(response['user']);
        _isAuthenticated = true;
      } else {
        // Token is invalid, clear stored data
        await _clearStoredData();
      }
    } catch (e) {
      // On error, clear stored data
      await _clearStoredData();
    }
  }
  
  // Check biometric authentication status
  Future<void> _checkBiometricStatus() async {
    try {
      final isAvailable = await _localAuth.canCheckBiometrics;
      final isDeviceSupported = await _localAuth.isDeviceSupported();
      
      if (isAvailable && isDeviceSupported) {
        final biometrics = await _localAuth.getAvailableBiometrics();
        _isBiometricEnabled = biometrics.isNotEmpty;
      } else {
        _isBiometricEnabled = false;
      }
    } catch (e) {
      _isBiometricEnabled = false;
    }
  }
  
  // Login with username and password
  Future<bool> login(String username, String password) async {
    try {
      _setLoading(true);
      _clearError();
      
      final response = await _apiService.login(username, password);
      
      if (response['success'] == true) {
        // Store tokens
        _authToken = response['access_token'];
        _refreshToken = response['refresh_token'];
        
        // Store tokens securely
        await _secureStorage.write(key: AppConfig.authTokenKey, value: _authToken);
        await _secureStorage.write(key: AppConfig.refreshTokenKey, value: _refreshToken);
        
        // Get user data
        await _fetchUserProfile();
        
        _isAuthenticated = true;
        notifyListeners();
        return true;
      } else {
        _setError(response['message'] ?? 'Login failed');
        return false;
      }
    } catch (e) {
      _setError('Login failed: $e');
      return false;
    } finally {
      _setLoading(false);
    }
  }
  
  // Login with biometric authentication
  Future<bool> loginWithBiometric() async {
    try {
      _setLoading(true);
      _clearError();
      
      // Check if biometric is available
      if (!_isBiometricEnabled) {
        _setError('Biometric authentication is not available');
        return false;
      }
      
      // Authenticate with biometric
      final isAuthenticated = await _localAuth.authenticate(
        localizedReason: 'Authenticate to access SML Professional',
        options: const AuthenticationOptions(
          stickyAuth: true,
          biometricOnly: true,
        ),
      );
      
      if (isAuthenticated) {
        // Load stored tokens
        await _loadStoredTokens();
        
        if (_authToken != null) {
          // Validate token
          await _validateToken();
          
          if (_isAuthenticated) {
            return true;
          }
        }
        
        _setError('Biometric authentication successful but no valid session found');
        return false;
      } else {
        _setError('Biometric authentication failed');
        return false;
      }
    } catch (e) {
      _setError('Biometric authentication error: $e');
      return false;
    } finally {
      _setLoading(false);
    }
  }
  
  // Fetch user profile from server
  Future<void> _fetchUserProfile() async {
    try {
      if (_authToken == null) return;
      
      final response = await _apiService.getUserProfile(_authToken!);
      
      if (response['success'] == true) {
        _currentUser = User.fromJson(response['user']);
        notifyListeners();
      }
    } catch (e) {
      _setError('Failed to fetch user profile: $e');
    }
  }
  
  // Setup biometric authentication
  Future<bool> setupBiometric() async {
    try {
      _setLoading(true);
      _clearError();
      
      // Check if biometric is available
      final isAvailable = await _localAuth.canCheckBiometrics;
      final isDeviceSupported = await _localAuth.isDeviceSupported();
      
      if (!isAvailable || !isDeviceSupported) {
        _setError('Biometric authentication is not supported on this device');
        return false;
      }
      
      // Get available biometrics
      final biometrics = await _localAuth.getAvailableBiometrics();
      
      if (biometrics.isEmpty) {
        _setError('No biometric authentication methods available');
        return false;
      }
      
      // Authenticate with biometric
      final isAuthenticated = await _localAuth.authenticate(
        localizedReason: 'Setup biometric authentication for SML Professional',
        options: const AuthenticationOptions(
          stickyAuth: true,
          biometricOnly: true,
        ),
      );
      
      if (isAuthenticated) {
        _isBiometricEnabled = true;
        
        // Store biometric preference
        await _secureStorage.write(
          key: 'biometric_enabled',
          value: 'true',
        );
        
        notifyListeners();
        return true;
      } else {
        _setError('Biometric setup failed');
        return false;
      }
    } catch (e) {
      _setError('Biometric setup error: $e');
      return false;
    } finally {
      _setLoading(false);
    }
  }
  
  // Refresh authentication token
  Future<bool> refreshToken() async {
    try {
      if (_refreshToken == null) return false;
      
      final response = await _apiService.refreshToken(_refreshToken!);
      
      if (response['success'] == true) {
        // Update tokens
        _authToken = response['access_token'];
        _refreshToken = response['refresh_token'];
        
        // Store new tokens
        await _secureStorage.write(key: AppConfig.authTokenKey, value: _authToken);
        await _secureStorage.write(key: AppConfig.refreshTokenKey, value: _refreshToken);
        
        notifyListeners();
        return true;
      } else {
        // Refresh failed, logout user
        await logout();
        return false;
      }
    } catch (e) {
      // On error, logout user
      await logout();
      return false;
    }
  }
  
  // Logout user
  Future<void> logout() async {
    try {
      _setLoading(true);
      
      // Call logout API if token exists
      if (_authToken != null) {
        try {
          await _apiService.logout(_authToken!);
        } catch (e) {
          // Ignore logout API errors
        }
      }
      
      // Clear stored data
      await _clearStoredData();
      
      // Reset state
      _currentUser = null;
      _authToken = null;
      _refreshToken = null;
      _isAuthenticated = false;
      _isBiometricEnabled = false;
      
      notifyListeners();
    } catch (e) {
      _setError('Logout failed: $e');
    } finally {
      _setLoading(false);
    }
  }
  
  // Clear stored data
  Future<void> _clearStoredData() async {
    try {
      await _secureStorage.delete(key: AppConfig.authTokenKey);
      await _secureStorage.delete(key: AppConfig.refreshTokenKey);
      await _secureStorage.delete(key: 'biometric_enabled');
    } catch (e) {
      // Ignore storage errors
    }
  }
  
  // Check authentication status
  Future<bool> checkAuthenticationStatus() async {
    try {
      if (_authToken == null) return false;
      
      // Validate token
      await _validateToken();
      return _isAuthenticated;
    } catch (e) {
      return false;
    }
  }
  
  // Check if biometric is enabled
  Future<bool> isBiometricEnabled() async {
    try {
      final enabled = await _secureStorage.read(key: 'biometric_enabled');
      _isBiometricEnabled = enabled == 'true';
      return _isBiometricEnabled;
    } catch (e) {
      return false;
    }
  }
  
  // Change password
  Future<bool> changePassword(String currentPassword, String newPassword) async {
    try {
      _setLoading(true);
      _clearError();
      
      if (_authToken == null) {
        _setError('Not authenticated');
        return false;
      }
      
      final response = await _apiService.changePassword(
        _authToken!,
        currentPassword,
        newPassword,
      );
      
      if (response['success'] == true) {
        return true;
      } else {
        _setError(response['message'] ?? 'Password change failed');
        return false;
      }
    } catch (e) {
      _setError('Password change failed: $e');
      return false;
    } finally {
      _setLoading(false);
    }
  }
  
  // Forgot password
  Future<bool> forgotPassword(String email) async {
    try {
      _setLoading(true);
      _clearError();
      
      final response = await _apiService.forgotPassword(email);
      
      if (response['success'] == true) {
        return true;
      } else {
        _setError(response['message'] ?? 'Password reset failed');
        return false;
      }
    } catch (e) {
      _setError('Password reset failed: $e');
      return false;
    } finally {
      _setLoading(false);
    }
  }
  
  // Reset password with OTP
  Future<bool> resetPassword(String email, String otp, String newPassword) async {
    try {
      _setLoading(true);
      _clearError();
      
      final response = await _apiService.resetPassword(email, otp, newPassword);
      
      if (response['success'] == true) {
        return true;
      } else {
        _setError(response['message'] ?? 'Password reset failed');
        return false;
      }
    } catch (e) {
      _setError('Password reset failed: $e');
      return false;
    } finally {
      _setLoading(false);
    }
  }
  
  // Update user profile
  Future<bool> updateProfile(Map<String, dynamic> profileData) async {
    try {
      _setLoading(true);
      _clearError();
      
      if (_authToken == null) {
        _setError('Not authenticated');
        return false;
      }
      
      final response = await _apiService.updateProfile(_authToken!, profileData);
      
      if (response['success'] == true) {
        // Update current user
        _currentUser = User.fromJson(response['user']);
        notifyListeners();
        return true;
      } else {
        _setError(response['message'] ?? 'Profile update failed');
        return false;
      }
    } catch (e) {
      _setError('Profile update failed: $e');
      return false;
    } finally {
      _setLoading(false);
    }
  }
  
  // Helper methods
  void _setLoading(bool loading) {
    _isLoading = loading;
    notifyListeners();
  }
  
  void _setError(String error) {
    _errorMessage = error;
    notifyListeners();
  }
  
  void _clearError() {
    _errorMessage = null;
    notifyListeners();
  }
  
  // Check if token is expired
  bool get isTokenExpired {
    if (_authToken == null) return true;
    
    try {
      // Decode JWT token to check expiration
      final parts = _authToken!.split('.');
      if (parts.length != 3) return true;
      
      final payload = parts[1];
      final normalized = base64Url.normalize(payload);
      final resp = utf8.decode(base64Url.decode(normalized));
      final payloadMap = json.decode(resp);
      
      final exp = payloadMap['exp'] as int?;
      if (exp == null) return true;
      
      final expiry = DateTime.fromMillisecondsSinceEpoch(exp * 1000);
      return DateTime.now().isAfter(expiry);
    } catch (e) {
      return true;
    }
  }
  
  // Auto-refresh token if needed
  Future<void> ensureValidToken() async {
    if (isTokenExpired && _refreshToken != null) {
      await refreshToken();
    }
  }
}

