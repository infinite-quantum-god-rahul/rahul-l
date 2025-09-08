import 'dart:convert';
import 'dart:io';
import 'package:dio/dio.dart';
import '../models/sml_models.dart';
import 'api_service.dart';

class SMLApiService extends ApiService {
  static final SMLApiService _instance = SMLApiService._internal();
  factory SMLApiService() => _instance;
  SMLApiService._internal();

  // SML Client Management
  Future<List<SMLClient>> getSMLClients({
    int? page,
    int? pageSize,
    String? search,
    String? status,
    String? sortBy,
    String? sortOrder,
  }) async {
    try {
      final queryParams = <String, dynamic>{};
      if (page != null) queryParams['page'] = page;
      if (pageSize != null) queryParams['page_size'] = pageSize;
      if (search != null) queryParams['search'] = search;
      if (status != null) queryParams['status'] = status;
      if (sortBy != null) queryParams['sort_by'] = sortBy;
      if (sortOrder != null) queryParams['sort_order'] = sortOrder;

      final response = await get('/api/sml-clients/', queryParameters: queryParams);
      final results = response['results'] as List;
      return results.map((json) => SMLClient.fromJson(json)).toList();
    } catch (e) {
      throw _handleApiError(e, 'Failed to fetch SML clients');
    }
  }

  Future<SMLClient> getSMLClient(int clientId) async {
    try {
      final response = await get('/api/sml-clients/$clientId/');
      return SMLClient.fromJson(response);
    } catch (e) {
      throw _handleApiError(e, 'Failed to fetch SML client');
    }
  }

  Future<SMLClient> createSMLClient(SMLClient client) async {
    try {
      final response = await post('/api/sml-clients/', client.toJson());
      return SMLClient.fromJson(response);
    } catch (e) {
      throw _handleApiError(e, 'Failed to create SML client');
    }
  }

  Future<SMLClient> updateSMLClient(int clientId, SMLClient client) async {
    try {
      final response = await put('/api/sml-clients/$clientId/', client.toJson());
      return SMLClient.fromJson(response);
    } catch (e) {
      throw _handleApiError(e, 'Failed to update SML client');
    }
  }

  Future<void> deleteSMLClient(int clientId) async {
    try {
      await delete('/api/sml-clients/$clientId/');
    } catch (e) {
      throw _handleApiError(e, 'Failed to delete SML client');
    }
  }

  // SML Loan Management
  Future<List<SMLLoanApplication>> getSMLLoans({
    int? page,
    int? pageSize,
    String? search,
    String? status,
    String? loanType,
    String? sortBy,
    String? sortOrder,
  }) async {
    try {
      final queryParams = <String, dynamic>{};
      if (page != null) queryParams['page'] = page;
      if (pageSize != null) queryParams['page_size'] = pageSize;
      if (search != null) queryParams['search'] = search;
      if (status != null) queryParams['status'] = status;
      if (loanType != null) queryParams['loan_type'] = loanType;
      if (sortBy != null) queryParams['sort_by'] = sortBy;
      if (sortOrder != null) queryParams['sort_order'] = sortOrder;

      final response = await get('/api/sml-loans/', queryParameters: queryParams);
      final results = response['results'] as List;
      return results.map((json) => SMLLoanApplication.fromJson(json)).toList();
    } catch (e) {
      throw _handleApiError(e, 'Failed to fetch SML loans');
    }
  }

  Future<SMLLoanApplication> getSMLLoan(int loanId) async {
    try {
      final response = await get('/api/sml-loans/$loanId/');
      return SMLLoanApplication.fromJson(response);
    } catch (e) {
      throw _handleApiError(e, 'Failed to fetch SML loan');
    }
  }

  Future<SMLLoanApplication> createSMLLoan(SMLLoanApplication loan) async {
    try {
      final response = await post('/api/sml-loans/', loan.toJson());
      return SMLLoanApplication.fromJson(response);
    } catch (e) {
      throw _handleApiError(e, 'Failed to create SML loan');
    }
  }

  Future<SMLLoanApplication> updateSMLLoan(int loanId, SMLLoanApplication loan) async {
    try {
      final response = await put('/api/sml-loans/$loanId/', loan.toJson());
      return SMLLoanApplication.fromJson(response);
    } catch (e) {
      throw _handleApiError(e, 'Failed to update SML loan');
    }
  }

  Future<void> deleteSMLLoan(int loanId) async {
    try {
      await delete('/api/sml-loans/$loanId/');
    } catch (e) {
      throw _handleApiError(e, 'Failed to delete SML loan');
    }
  }

  // SML Field Operations
  Future<List<SMLFieldVisit>> getSMLFieldVisits({
    int? page,
    int? pageSize,
    String? search,
    String? status,
    String? priority,
    String? sortBy,
    String? sortOrder,
  }) async {
    try {
      final queryParams = <String, dynamic>{};
      if (page != null) queryParams['page'] = page;
      if (pageSize != null) queryParams['page_size'] = pageSize;
      if (search != null) queryParams['search'] = search;
      if (status != null) queryParams['status'] = status;
      if (priority != null) queryParams['priority'] = priority;
      if (sortBy != null) queryParams['sort_by'] = sortBy;
      if (sortOrder != null) queryParams['sort_order'] = sortOrder;

      final response = await get('/api/sml-field-visits/', queryParameters: queryParams);
      final results = response['results'] as List;
      return results.map((json) => SMLFieldVisit.fromJson(json)).toList();
    } catch (e) {
      throw _handleApiError(e, 'Failed to fetch SML field visits');
    }
  }

  Future<SMLFieldVisit> getSMLFieldVisit(int visitId) async {
    try {
      final response = await get('/api/sml-field-visits/$visitId/');
      return SMLFieldVisit.fromJson(response);
    } catch (e) {
      throw _handleApiError(e, 'Failed to fetch SML field visit');
    }
  }

  Future<SMLFieldVisit> createSMLFieldVisit(SMLFieldVisit visit) async {
    try {
      final response = await post('/api/sml-field-visits/', visit.toJson());
      return SMLFieldVisit.fromJson(response);
    } catch (e) {
      throw _handleApiError(e, 'Failed to create SML field visit');
    }
  }

  Future<SMLFieldVisit> updateSMLFieldVisit(int visitId, SMLFieldVisit visit) async {
    try {
      final response = await put('/api/sml-field-visits/$visitId/', visit.toJson());
      return SMLFieldVisit.fromJson(response);
    } catch (e) {
      throw _handleApiError(e, 'Failed to update SML field visit');
    }
  }

  Future<void> deleteSMLFieldVisit(int visitId) async {
    try {
      await delete('/api/sml-field-visits/$visitId/');
    } catch (e) {
      throw _handleApiError(e, 'Failed to delete SML field visit');
    }
  }

  Future<List<SMLFieldSchedule>> getSMLFieldSchedules({
    int? page,
    int? pageSize,
    String? search,
    String? status,
    String? priority,
    String? sortBy,
    String? sortOrder,
  }) async {
    try {
      final queryParams = <String, dynamic>{};
      if (page != null) queryParams['page'] = page;
      if (pageSize != null) queryParams['page_size'] = pageSize;
      if (search != null) queryParams['search'] = search;
      if (status != null) queryParams['status'] = status;
      if (priority != null) queryParams['priority'] = priority;
      if (sortBy != null) queryParams['sort_by'] = sortBy;
      if (sortOrder != null) queryParams['sort_order'] = sortOrder;

      final response = await get('/api/sml-field-schedules/', queryParameters: queryParams);
      final results = response['results'] as List;
      return results.map((json) => SMLFieldSchedule.fromJson(json)).toList();
    } catch (e) {
      throw _handleApiError(e, 'Failed to fetch SML field schedules');
    }
  }

  // SML Reports and Analytics
  Future<Map<String, dynamic>> getSMLDashboardStats() async {
    try {
      final response = await get('/api/dashboard/stats/');
      return response;
    } catch (e) {
      throw _handleApiError(e, 'Failed to fetch SML dashboard stats');
    }
  }

  Future<Map<String, dynamic>> getSMLAnalytics({
    String? period,
    String? type,
    String? groupBy,
  }) async {
    try {
      final queryParams = <String, dynamic>{};
      if (period != null) queryParams['period'] = period;
      if (type != null) queryParams['type'] = type;
      if (groupBy != null) queryParams['group_by'] = groupBy;

      final response = await get('/api/analytics/', queryParameters: queryParams);
      return response;
    } catch (e) {
      throw _handleApiError(e, 'Failed to fetch SML analytics');
    }
  }

  Future<List<Map<String, dynamic>>> getSMLReports({
    int? page,
    int? pageSize,
    String? reportType,
    String? status,
    String? dateFrom,
    String? dateTo,
  }) async {
    try {
      final queryParams = <String, dynamic>{};
      if (page != null) queryParams['page'] = page;
      if (pageSize != null) queryParams['page_size'] = pageSize;
      if (reportType != null) queryParams['report_type'] = reportType;
      if (status != null) queryParams['status'] = status;
      if (dateFrom != null) queryParams['date_from'] = dateFrom;
      if (dateTo != null) queryParams['date_to'] = dateTo;

      final response = await get('/api/reports/', queryParameters: queryParams);
      final results = response['results'] as List;
      return results.cast<Map<String, dynamic>>();
    } catch (e) {
      throw _handleApiError(e, 'Failed to fetch SML reports');
    }
  }

  // SML Document Management
  Future<List<SMLKYCDocument>> getSMLKYCDocuments({
    int? page,
    int? pageSize,
    String? search,
    String? documentType,
    String? status,
  }) async {
    try {
      final queryParams = <String, dynamic>{};
      if (page != null) queryParams['page'] = page;
      if (pageSize != null) queryParams['page_size'] = pageSize;
      if (search != null) queryParams['search'] = search;
      if (documentType != null) queryParams['document_type'] = documentType;
      if (status != null) queryParams['status'] = status;

      final response = await get('/api/sml-kyc-documents/', queryParameters: queryParams);
      final results = response['results'] as List;
      return results.map((json) => SMLKYCDocument.fromJson(json)).toList();
    } catch (e) {
      throw _handleApiError(e, 'Failed to fetch SML KYC documents');
    }
  }

  Future<SMLKYCDocument> uploadSMLKYCDocument(
    int clientId,
    String documentType,
    File file,
    String description,
  ) async {
    try {
      final formData = FormData.fromMap({
        'client': clientId.toString(),
        'document_type': documentType,
        'file': await MultipartFile.fromFile(file.path),
        'description': description,
      });

      final response = await post('/api/sml-kyc-documents/', formData);
      return SMLKYCDocument.fromJson(response);
    } catch (e) {
      throw _handleApiError(e, 'Failed to upload SML KYC document');
    }
  }

  // SML Search
  Future<Map<String, dynamic>> searchSMLEntities(String query, {
    List<String>? entityTypes,
    int? limit,
  }) async {
    try {
      final queryParams = <String, dynamic>{
        'q': query,
      };
      if (entityTypes != null) queryParams['entity_types'] = entityTypes.join(',');
      if (limit != null) queryParams['limit'] = limit;

      final response = await get('/api/search/', queryParameters: queryParams);
      return response;
    } catch (e) {
      throw _handleApiError(e, 'Failed to search SML entities');
    }
  }

  // SML Offline Sync
  Future<Map<String, dynamic>> syncSMLData(Map<String, dynamic> offlineData) async {
    try {
      final response = await post('/api/sync/', offlineData);
      return response;
    } catch (e) {
      throw _handleApiError(e, 'Failed to sync SML data');
    }
  }

  // Error handling helper
  Exception _handleApiError(dynamic error, String defaultMessage) {
    if (error is DioException) {
      switch (error.type) {
        case DioExceptionType.connectionTimeout:
        case DioExceptionType.receiveTimeout:
        case DioExceptionType.sendTimeout:
          return Exception('Connection timeout. Please check your internet connection.');
        case DioExceptionType.badResponse:
          final statusCode = error.response?.statusCode;
          final message = error.response?.data?['message'] ?? defaultMessage;
          return Exception('Error $statusCode: $message');
        case DioExceptionType.cancel:
          return Exception('Request was cancelled.');
        case DioExceptionType.connectionError:
          return Exception('No internet connection. Please check your network.');
        default:
          return Exception(defaultMessage);
      }
    }
    return Exception(defaultMessage);
  }
}

