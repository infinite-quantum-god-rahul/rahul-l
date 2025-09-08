import 'dart:convert';
import 'dart:io';
import 'package:http/http.dart' as http;
import 'package:dio/dio.dart';
import 'package:connectivity_plus/connectivity_plus.dart';
import '../config/app_config.dart';
import '../utils/constants.dart';
import '../utils/network_utils.dart';

class ApiService {
  static final ApiService _instance = ApiService._internal();
  factory ApiService() => _instance;
  ApiService._internal();
  
  late Dio _dio;
  late http.Client _httpClient;
  
  // Initialize the service
  void initialize() {
    _dio = Dio(BaseOptions(
      baseUrl: AppConfig.apiBaseUrl,
      connectTimeout: Duration(milliseconds: AppConfig.apiTimeout),
      receiveTimeout: Duration(milliseconds: AppConfig.apiTimeout),
      headers: {
        'Content-Type': 'application/json',
        'Accept': 'application/json',
        'User-Agent': 'SML-Professional-Mobile/${AppConfig.appVersion}',
      },
    ));
    
    _httpClient = http.Client();
    
    // Add interceptors
    _setupInterceptors();
  }
  
  // Setup Dio interceptors
  void _setupInterceptors() {
    // Request interceptor
    _dio.interceptors.add(InterceptorsWrapper(
      onRequest: (options, handler) async {
        // Add authentication token if available
        final token = await _getStoredToken();
        if (token != null) {
          options.headers['Authorization'] = 'Bearer $token';
        }
        
        // Log request
        if (AppConfig.enableDebugLogs) {
          print('API Request: ${options.method} ${options.path}');
          print('Headers: ${options.headers}');
          if (options.data != null) {
            print('Data: ${options.data}');
          }
        }
        
        handler.next(options);
      },
      
      onResponse: (response, handler) async {
        // Log response
        if (AppConfig.enableDebugLogs) {
          print('API Response: ${response.statusCode} ${response.requestOptions.path}');
          print('Data: ${response.data}');
        }
        
        handler.next(response);
      },
      
      onError: (error, handler) async {
        // Handle token expiration
        if (error.response?.statusCode == 401) {
          final refreshed = await _refreshToken();
          if (refreshed) {
            // Retry the original request
            final retryResponse = await _dio.request(
              error.requestOptions.path,
              data: error.requestOptions.data,
              queryParameters: error.requestOptions.queryParameters,
              options: Options(
                method: error.requestOptions.method,
                headers: error.requestOptions.headers,
              ),
            );
            handler.resolve(retryResponse);
            return;
          }
        }
        
        // Log error
        if (AppConfig.enableDebugLogs) {
          print('API Error: ${error.message}');
          print('Status: ${error.response?.statusCode}');
          print('Data: ${error.response?.data}');
        }
        
        handler.next(error);
      },
    ));
  }
  
  // Get stored authentication token
  Future<String?> _getStoredToken() async {
    // This would typically come from secure storage
    // For now, return null
    return null;
  }
  
  // Refresh authentication token
  Future<bool> _refreshToken() async {
    try {
      final refreshToken = await _getStoredRefreshToken();
      if (refreshToken == null) return false;
      
      final response = await _dio.post('/auth/refresh/', data: {
        'refresh_token': refreshToken,
      });
      
      if (response.statusCode == 200) {
        // Store new tokens
        await _storeTokens(
          response.data['access_token'],
          response.data['refresh_token'],
        );
        return true;
      }
      
      return false;
    } catch (e) {
      return false;
    }
  }
  
  // Get stored refresh token
  Future<String?> _getStoredRefreshToken() async {
    // This would typically come from secure storage
    // For now, return null
    return null;
  }
  
  // Store authentication tokens
  Future<void> _storeTokens(String accessToken, String refreshToken) async {
    // This would typically store in secure storage
    // For now, do nothing
  }
  
  // Check network connectivity
  Future<bool> _checkConnectivity() async {
    final connectivityResult = await Connectivity().checkConnectivity();
    return connectivityResult != ConnectivityResult.none;
  }
  
  // Generic GET request
  Future<Map<String, dynamic>> get(String endpoint, {
    Map<String, String>? headers,
    Map<String, dynamic>? queryParameters,
  }) async {
    try {
      // Check connectivity
      if (!await _checkConnectivity()) {
        throw Exception('No internet connection');
      }
      
      final response = await _dio.get(
        endpoint,
        options: Options(headers: headers),
        queryParameters: queryParameters,
      );
      
      return _handleResponse(response);
    } catch (e) {
      return _handleError(e);
    }
  }
  
  // Generic POST request
  Future<Map<String, dynamic>> post(String endpoint, {
    dynamic data,
    Map<String, String>? headers,
    Map<String, dynamic>? queryParameters,
  }) async {
    try {
      // Check connectivity
      if (!await _checkConnectivity()) {
        throw Exception('No internet connection');
      }
      
      final response = await _dio.post(
        endpoint,
        data: data,
        options: Options(headers: headers),
        queryParameters: queryParameters,
      );
      
      return _handleResponse(response);
    } catch (e) {
      return _handleError(e);
    }
  }
  
  // Generic PUT request
  Future<Map<String, dynamic>> put(String endpoint, {
    dynamic data,
    Map<String, String>? headers,
    Map<String, dynamic>? queryParameters,
  }) async {
    try {
      // Check connectivity
      if (!await _checkConnectivity()) {
        throw Exception('No internet connection');
      }
      
      final response = await _dio.put(
        endpoint,
        data: data,
        options: Options(headers: headers),
        queryParameters: queryParameters,
      );
      
      return _handleResponse(response);
    } catch (e) {
      return _handleError(e);
    }
  }
  
  // Generic DELETE request
  Future<Map<String, dynamic>> delete(String endpoint, {
    Map<String, String>? headers,
    Map<String, dynamic>? queryParameters,
  }) async {
    try {
      // Check connectivity
      if (!await _checkConnectivity()) {
        throw Exception('No internet connection');
      }
      
      final response = await _dio.delete(
        endpoint,
        options: Options(headers: headers),
        queryParameters: queryParameters,
      );
      
      return _handleResponse(response);
    } catch (e) {
      return _handleError(e);
    }
  }
  
  // File upload request
  Future<Map<String, dynamic>> uploadFile(String endpoint, {
    required String filePath,
    required String fieldName,
    Map<String, String>? additionalData,
    Map<String, String>? headers,
    void Function(int, int)? onProgress,
  }) async {
    try {
      // Check connectivity
      if (!await _checkConnectivity()) {
        throw Exception('No internet connection');
      }
      
      // Check file exists
      final file = File(filePath);
      if (!await file.exists()) {
        throw Exception('File not found: $filePath');
      }
      
      // Check file size
      final fileSize = await file.length();
      if (fileSize > AppConfig.maxFileSize) {
        throw Exception('File size exceeds limit: ${AppConfig.maxFileSize} bytes');
      }
      
      // Create form data
      final formData = FormData.fromMap({
        fieldName: await MultipartFile.fromFile(filePath),
        ...?additionalData,
      });
      
      final response = await _dio.post(
        endpoint,
        data: formData,
        options: Options(headers: headers),
        onSendProgress: onProgress,
      );
      
      return _handleResponse(response);
    } catch (e) {
      return _handleError(e);
    }
  }
  
  // Handle successful response
  Map<String, dynamic> _handleResponse(Response response) {
    if (response.statusCode! >= 200 && response.statusCode! < 300) {
      if (response.data is Map<String, dynamic>) {
        return response.data;
      } else if (response.data is String) {
        try {
          return json.decode(response.data);
        } catch (e) {
          return {'success': true, 'data': response.data};
        }
      } else {
        return {'success': true, 'data': response.data};
      }
    } else {
      throw DioException(
        requestOptions: response.requestOptions,
        response: response,
        type: DioExceptionType.badResponse,
      );
    }
  }
  
  // Handle error response
  Map<String, dynamic> _handleError(dynamic error) {
    if (error is DioException) {
      switch (error.type) {
        case DioExceptionType.connectionTimeout:
        case DioExceptionType.sendTimeout:
        case DioExceptionType.receiveTimeout:
          return {
            'success': false,
            'message': 'Request timeout. Please try again.',
            'error': 'timeout',
          };
        
        case DioExceptionType.badResponse:
          final statusCode = error.response?.statusCode;
          final data = error.response?.data;
          
          switch (statusCode) {
            case 400:
              return {
                'success': false,
                'message': data?['message'] ?? 'Bad request',
                'error': 'bad_request',
                'details': data,
              };
            
            case 401:
              return {
                'success': false,
                'message': 'Unauthorized. Please login again.',
                'error': 'unauthorized',
              };
            
            case 403:
              return {
                'success': false,
                'message': 'Access denied. You don\'t have permission.',
                'error': 'forbidden',
              };
            
            case 404:
              return {
                'success': false,
                'message': 'Resource not found.',
                'error': 'not_found',
              };
            
            case 422:
              return {
                'success': false,
                'message': data?['message'] ?? 'Validation failed',
                'error': 'validation_error',
                'details': data,
              };
            
            case 500:
              return {
                'success': false,
                'message': 'Server error. Please try again later.',
                'error': 'server_error',
              };
            
            default:
              return {
                'success': false,
                'message': 'An error occurred. Please try again.',
                'error': 'unknown_error',
                'status_code': statusCode,
              };
          }
        
        case DioExceptionType.cancel:
          return {
            'success': false,
            'message': 'Request cancelled.',
            'error': 'cancelled',
          };
        
        case DioExceptionType.connectionError:
          return {
            'success': false,
            'message': 'No internet connection.',
            'error': 'connection_error',
          };
        
        default:
          return {
            'success': false,
            'message': 'An error occurred. Please try again.',
            'error': 'unknown_error',
          };
      }
    } else if (error is SocketException) {
      return {
        'success': false,
        'message': 'No internet connection.',
        'error': 'connection_error',
      };
    } else {
      return {
        'success': false,
        'message': 'An unexpected error occurred.',
        'error': 'unexpected_error',
        'details': error.toString(),
      };
    }
  }
  
  // Authentication API methods
  
  // Login
  Future<Map<String, dynamic>> login(String username, String password) async {
    return await post('/auth/login/', data: {
      'username': username,
      'password': password,
    });
  }
  
  // Logout
  Future<Map<String, dynamic>> logout(String token) async {
    return await post('/auth/logout/', headers: {
      'Authorization': 'Bearer $token',
    });
  }
  
  // Refresh token
  Future<Map<String, dynamic>> refreshToken(String refreshToken) async {
    return await post('/auth/refresh/', data: {
      'refresh_token': refreshToken,
    });
  }
  
  // Validate token
  Future<Map<String, dynamic>> validateToken(String token) async {
    return await get('/auth/validate/', headers: {
      'Authorization': 'Bearer $token',
    });
  }
  
  // Get user profile
  Future<Map<String, dynamic>> getUserProfile(String token) async {
    return await get('/auth/profile/', headers: {
      'Authorization': 'Bearer $token',
    });
  }
  
  // Change password
  Future<Map<String, dynamic>> changePassword(
    String token,
    String currentPassword,
    String newPassword,
  ) async {
    return await post('/auth/change-password/', data: {
      'current_password': currentPassword,
      'new_password': newPassword,
    }, headers: {
      'Authorization': 'Bearer $token',
    });
  }
  
  // Forgot password
  Future<Map<String, dynamic>> forgotPassword(String email) async {
    return await post('/auth/forgot-password/', data: {
      'email': email,
    });
  }
  
  // Reset password
  Future<Map<String, dynamic>> resetPassword(
    String email,
    String otp,
    String newPassword,
  ) async {
    return await post('/auth/reset-password/', data: {
      'email': email,
      'otp': otp,
      'new_password': newPassword,
    });
  }
  
  // Update profile
  Future<Map<String, dynamic>> updateProfile(
    String token,
    Map<String, dynamic> profileData,
  ) async {
    return await put('/auth/profile/', data: profileData, headers: {
      'Authorization': 'Bearer $token',
    });
  }
  
  // Client Management API methods
  
  // Get clients list
  Future<Map<String, dynamic>> getClients({
    int? page,
    int? pageSize,
    String? search,
    String? status,
    String? token,
  }) async {
    final queryParams = <String, dynamic>{};
    if (page != null) queryParams['page'] = page;
    if (pageSize != null) queryParams['page_size'] = pageSize;
    if (search != null) queryParams['search'] = search;
    if (status != null) queryParams['status'] = status;
    
    return await get('/clients/', 
      queryParameters: queryParams,
      headers: token != null ? {'Authorization': 'Bearer $token'} : null,
    );
  }
  
  // Get client details
  Future<Map<String, dynamic>> getClient(int clientId, {String? token}) async {
    return await get('/clients/$clientId/', 
      headers: token != null ? {'Authorization': 'Bearer $token'} : null,
    );
  }
  
  // Create client
  Future<Map<String, dynamic>> createClient(
    Map<String, dynamic> clientData,
    {String? token}
  ) async {
    return await post('/clients/', 
      data: clientData,
      headers: token != null ? {'Authorization': 'Bearer $token'} : null,
    );
  }
  
  // Update client
  Future<Map<String, dynamic>> updateClient(
    int clientId,
    Map<String, dynamic> clientData,
    {String? token}
  ) async {
    return await put('/clients/$clientId/', 
      data: clientData,
      headers: token != null ? {'Authorization': 'Bearer $token'} : null,
    );
  }
  
  // Delete client
  Future<Map<String, dynamic>> deleteClient(int clientId, {String? token}) async {
    return await delete('/clients/$clientId/', 
      headers: token != null ? {'Authorization': 'Bearer $token'} : null,
    );
  }
  
  // Loan Management API methods
  
  // Get loans list
  Future<Map<String, dynamic>> getLoans({
    int? page,
    int? pageSize,
    String? search,
    String? status,
    String? token,
  }) async {
    final queryParams = <String, dynamic>{};
    if (page != null) queryParams['page'] = page;
    if (pageSize != null) queryParams['page_size'] = pageSize;
    if (search != null) queryParams['search'] = search;
    if (status != null) queryParams['status'] = status;
    
    return await get('/loans/', 
      queryParameters: queryParams,
      headers: token != null ? {'Authorization': 'Bearer $token'} : null,
    );
  }
  
  // Get loan details
  Future<Map<String, dynamic>> getLoan(int loanId, {String? token}) async {
    return await get('/loans/$loanId/', 
      headers: token != null ? {'Authorization': 'Bearer $token'} : null,
    );
  }
  
  // Create loan
  Future<Map<String, dynamic>> createLoan(
    Map<String, dynamic> loanData,
    {String? token}
  ) async {
    return await post('/loans/', 
      data: loanData,
      headers: token != null ? {'Authorization': 'Bearer $token'} : null,
    );
  }
  
  // Update loan
  Future<Map<String, dynamic>> updateLoan(
    int loanId,
    Map<String, dynamic> loanData,
    {String? token}
  ) async {
    return await put('/loans/$loanId/', 
      data: loanData,
      headers: token != null ? {'Authorization': 'Bearer $token'} : null,
    );
  }
  
  // Delete loan
  Future<Map<String, dynamic>> deleteLoan(int loanId, {String? token}) async {
    return await delete('/loans/$loanId/', 
      headers: token != null ? {'Authorization': 'Bearer $token'} : null,
    );
  }
  
  // Field Operations API methods
  
  // Get field schedule
  Future<Map<String, dynamic>> getFieldSchedule({
    int? page,
    int? pageSize,
    String? date,
    String? status,
    String? token,
  }) async {
    final queryParams = <String, dynamic>{};
    if (page != null) queryParams['page'] = page;
    if (pageSize != null) queryParams['page_size'] = pageSize;
    if (date != null) queryParams['date'] = date;
    if (status != null) queryParams['status'] = status;
    
    return await get('/field/schedule/', 
      queryParameters: queryParams,
      headers: token != null ? {'Authorization': 'Bearer $token'} : null,
    );
  }
  
  // Get field visit details
  Future<Map<String, dynamic>> getFieldVisit(int visitId, {String? token}) async {
    return await get('/field/visits/$visitId/', 
      headers: token != null ? {'Authorization': 'Bearer $token'} : null,
    );
  }
  
  // Create field visit
  Future<Map<String, dynamic>> createFieldVisit(
    Map<String, dynamic> visitData,
    {String? token}
  ) async {
    return await post('/field/visits/', 
      data: visitData,
      headers: token != null ? {'Authorization': 'Bearer $token'} : null,
    );
  }
  
  // Update field visit
  Future<Map<String, dynamic>> updateFieldVisit(
    int visitId,
    Map<String, dynamic> visitData,
    {String? token}
  ) async {
    return await put('/field/visits/$visitId/', 
      data: visitData,
      headers: token != null ? {'Authorization': 'Bearer $token'} : null,
    );
  }
  
  // Reports API methods
  
  // Get dashboard stats
  Future<Map<String, dynamic>> getDashboardStats({String? token}) async {
    return await get('/reports/dashboard/', 
      headers: token != null ? {'Authorization': 'Bearer $token'} : null,
    );
  }
  
  // Get analytics data
  Future<Map<String, dynamic>> getAnalytics({
    String? type,
    String? period,
    String? token,
  }) async {
    final queryParams = <String, dynamic>{};
    if (type != null) queryParams['type'] = type;
    if (period != null) queryParams['period'] = period;
    
    return await get('/reports/analytics/', 
      queryParameters: queryParams,
      headers: token != null ? {'Authorization': 'Bearer $token'} : null,
    );
  }
  
  // Export report
  Future<Map<String, dynamic>> exportReport({
    required String reportType,
    Map<String, dynamic>? filters,
    String? format,
    String? token,
  }) async {
    final data = <String, dynamic>{
      'report_type': reportType,
      if (filters != null) 'filters': filters,
      if (format != null) 'format': format,
    };
    
    return await post('/reports/export/', 
      data: data,
      headers: token != null ? {'Authorization': 'Bearer $token'} : null,
    );
  }
  
  // Dispose resources
  void dispose() {
    _dio.close();
    _httpClient.close();
  }
}

