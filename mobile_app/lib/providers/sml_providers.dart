import 'package:flutter/foundation.dart';
import '../models/sml_models.dart';
import '../services/sml_api_service.dart';

// SML Client Provider
class SMLClientProvider extends ChangeNotifier {
  final SMLApiService _apiService = SMLApiService();
  
  List<SMLClient> _clients = [];
  SMLClient? _selectedClient;
  bool _isLoading = false;
  String? _errorMessage;
  int _currentPage = 1;
  bool _hasMoreData = true;
  String _searchQuery = '';
  String _statusFilter = '';

  // Getters
  List<SMLClient> get clients => _clients;
  SMLClient? get selectedClient => _selectedClient;
  bool get isLoading => _isLoading;
  String? get errorMessage => _errorMessage;
  bool get hasMoreData => _hasMoreData;
  String get searchQuery => _searchQuery;
  String get statusFilter => _statusFilter;

  // Load clients with pagination
  Future<void> loadClients({bool refresh = false}) async {
    if (refresh) {
      _currentPage = 1;
      _clients.clear();
      _hasMoreData = true;
    }

    if (!_hasMoreData || _isLoading) return;

    try {
      _setLoading(true);
      _clearError();

      final newClients = await _apiService.getSMLClients(
        page: _currentPage,
        pageSize: 20,
        search: _searchQuery.isNotEmpty ? _searchQuery : null,
        status: _statusFilter.isNotEmpty ? _statusFilter : null,
        sortBy: 'created_at',
        sortOrder: 'desc',
      );

      if (refresh) {
        _clients = newClients;
      } else {
        _clients.addAll(newClients);
      }

      _hasMoreData = newClients.length == 20;
      _currentPage++;
    } catch (e) {
      _setError(e.toString());
    } finally {
      _setLoading(false);
    }
  }

  // Search clients
  Future<void> searchClients(String query) async {
    _searchQuery = query;
    await loadClients(refresh: true);
  }

  // Filter clients by status
  Future<void> filterClientsByStatus(String status) async {
    _statusFilter = status;
    await loadClients(refresh: true);
  }

  // Get single client
  Future<SMLClient?> getClient(int clientId) async {
    try {
      _setLoading(true);
      _clearError();
      
      final client = await _apiService.getSMLClient(clientId);
      _selectedClient = client;
      return client;
    } catch (e) {
      _setError(e.toString());
      return null;
    } finally {
      _setLoading(false);
    }
  }

  // Create new client
  Future<bool> createClient(SMLClient client) async {
    try {
      _setLoading(true);
      _clearError();
      
      final newClient = await _apiService.createSMLClient(client);
      _clients.insert(0, newClient);
      notifyListeners();
      return true;
    } catch (e) {
      _setError(e.toString());
      return false;
    } finally {
      _setLoading(false);
    }
  }

  // Update client
  Future<bool> updateClient(int clientId, SMLClient client) async {
    try {
      _setLoading(true);
      _clearError();
      
      final updatedClient = await _apiService.updateSMLClient(clientId, client);
      
      final index = _clients.indexWhere((c) => c.id == clientId);
      if (index != -1) {
        _clients[index] = updatedClient;
      }
      
      if (_selectedClient?.id == clientId) {
        _selectedClient = updatedClient;
      }
      
      notifyListeners();
      return true;
    } catch (e) {
      _setError(e.toString());
      return false;
    } finally {
      _setLoading(false);
    }
  }

  // Delete client
  Future<bool> deleteClient(int clientId) async {
    try {
      _setLoading(true);
      _clearError();
      
      await _apiService.deleteSMLClient(clientId);
      
      _clients.removeWhere((c) => c.id == clientId);
      if (_selectedClient?.id == clientId) {
        _selectedClient = null;
      }
      
      notifyListeners();
      return true;
    } catch (e) {
      _setError(e.toString());
      return false;
    } finally {
      _setLoading(false);
    }
  }

  // Select client
  void selectClient(SMLClient? client) {
    _selectedClient = client;
    notifyListeners();
  }

  // Clear error
  void clearError() {
    _errorMessage = null;
    notifyListeners();
  }

  // Private methods
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
  }
}

// SML Loan Provider
class SMLLoanProvider extends ChangeNotifier {
  final SMLApiService _apiService = SMLApiService();
  
  List<SMLLoanApplication> _loans = [];
  SMLLoanApplication? _selectedLoan;
  bool _isLoading = false;
  String? _errorMessage;
  int _currentPage = 1;
  bool _hasMoreData = true;
  String _searchQuery = '';
  String _statusFilter = '';
  String _loanTypeFilter = '';

  // Getters
  List<SMLLoanApplication> get loans => _loans;
  SMLLoanApplication? get selectedLoan => _selectedLoan;
  bool get isLoading => _isLoading;
  String? get errorMessage => _errorMessage;
  bool get hasMoreData => _hasMoreData;
  String get searchQuery => _searchQuery;
  String get statusFilter => _statusFilter;
  String get loanTypeFilter => _loanTypeFilter;

  // Load loans with pagination
  Future<void> loadLoans({bool refresh = false}) async {
    if (refresh) {
      _currentPage = 1;
      _loans.clear();
      _hasMoreData = true;
    }

    if (!_hasMoreData || _isLoading) return;

    try {
      _setLoading(true);
      _clearError();

      final newLoans = await _apiService.getSMLLoans(
        page: _currentPage,
        pageSize: 20,
        search: _searchQuery.isNotEmpty ? _searchQuery : null,
        status: _statusFilter.isNotEmpty ? _statusFilter : null,
        loanType: _loanTypeFilter.isNotEmpty ? _loanTypeFilter : null,
        sortBy: 'created_at',
        sortOrder: 'desc',
      );

      if (refresh) {
        _loans = newLoans;
      } else {
        _loans.addAll(newLoans);
      }

      _hasMoreData = newLoans.length == 20;
      _currentPage++;
    } catch (e) {
      _setError(e.toString());
    } finally {
      _setLoading(false);
    }
  }

  // Search loans
  Future<void> searchLoans(String query) async {
    _searchQuery = query;
    await loadLoans(refresh: true);
  }

  // Filter loans by status
  Future<void> filterLoansByStatus(String status) async {
    _statusFilter = status;
    await loadLoans(refresh: true);
  }

  // Filter loans by type
  Future<void> filterLoansByType(String loanType) async {
    _loanTypeFilter = loanType;
    await loadLoans(refresh: true);
  }

  // Get single loan
  Future<SMLLoanApplication?> getLoan(int loanId) async {
    try {
      _setLoading(true);
      _clearError();
      
      final loan = await _apiService.getSMLLoan(loanId);
      _selectedLoan = loan;
      return loan;
    } catch (e) {
      _setError(e.toString());
      return null;
    } finally {
      _setLoading(false);
    }
  }

  // Create new loan
  Future<bool> createLoan(SMLLoanApplication loan) async {
    try {
      _setLoading(true);
      _clearError();
      
      final newLoan = await _apiService.createSMLLoan(loan);
      _loans.insert(0, newLoan);
      notifyListeners();
      return true;
    } catch (e) {
      _setError(e.toString());
      return false;
    } finally {
      _setLoading(false);
    }
  }

  // Update loan
  Future<bool> updateLoan(int loanId, SMLLoanApplication loan) async {
    try {
      _setLoading(true);
      _clearError();
      
      final updatedLoan = await _apiService.updateSMLLoan(loanId, loan);
      
      final index = _loans.indexWhere((l) => l.id == loanId);
      if (index != -1) {
        _loans[index] = updatedLoan;
      }
      
      if (_selectedLoan?.id == loanId) {
        _selectedLoan = updatedLoan;
      }
      
      notifyListeners();
      return true;
    } catch (e) {
      _setError(e.toString());
      return false;
    } finally {
      _setLoading(false);
    }
  }

  // Delete loan
  Future<bool> deleteLoan(int loanId) async {
    try {
      _setLoading(true);
      _clearError();
      
      await _apiService.deleteSMLLoan(loanId);
      
      _loans.removeWhere((l) => l.id == loanId);
      if (_selectedLoan?.id == loanId) {
        _selectedLoan = null;
      }
      
      notifyListeners();
      return true;
    } catch (e) {
      _setError(e.toString());
      return false;
    } finally {
      _setLoading(false);
    }
  }

  // Select loan
  void selectLoan(SMLLoanApplication? loan) {
    _selectedLoan = loan;
    notifyListeners();
  }

  // Clear error
  void clearError() {
    _errorMessage = null;
    notifyListeners();
  }

  // Private methods
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
  }
}

// SML Field Operations Provider
class SMLFieldOperationsProvider extends ChangeNotifier {
  final SMLApiService _apiService = SMLApiService();
  
  List<SMLFieldVisit> _fieldVisits = [];
  List<SMLFieldSchedule> _fieldSchedules = [];
  SMLFieldVisit? _selectedVisit;
  SMLFieldSchedule? _selectedSchedule;
  bool _isLoading = false;
  String? _errorMessage;
  int _currentPage = 1;
  bool _hasMoreData = true;
  String _searchQuery = '';
  String _statusFilter = '';
  String _priorityFilter = '';

  // Getters
  List<SMLFieldVisit> get fieldVisits => _fieldVisits;
  List<SMLFieldSchedule> get fieldSchedules => _fieldSchedules;
  SMLFieldVisit? get selectedVisit => _selectedVisit;
  SMLFieldSchedule? get selectedSchedule => _selectedSchedule;
  bool get isLoading => _isLoading;
  String? get errorMessage => _errorMessage;
  bool get hasMoreData => _hasMoreData;
  String get searchQuery => _searchQuery;
  String get statusFilter => _statusFilter;
  String get priorityFilter => _priorityFilter;

  // Load field visits with pagination
  Future<void> loadFieldVisits({bool refresh = false}) async {
    if (refresh) {
      _currentPage = 1;
      _fieldVisits.clear();
      _hasMoreData = true;
    }

    if (!_hasMoreData || _isLoading) return;

    try {
      _setLoading(true);
      _clearError();

      final newVisits = await _apiService.getSMLFieldVisits(
        page: _currentPage,
        pageSize: 20,
        search: _searchQuery.isNotEmpty ? _searchQuery : null,
        status: _statusFilter.isNotEmpty ? _statusFilter : null,
        priority: _priorityFilter.isNotEmpty ? _priorityFilter : null,
        sortBy: 'scheduled_date',
        sortOrder: 'asc',
      );

      if (refresh) {
        _fieldVisits = newVisits;
      } else {
        _fieldVisits.addAll(newVisits);
      }

      _hasMoreData = newVisits.length == 20;
      _currentPage++;
    } catch (e) {
      _setError(e.toString());
    } finally {
      _setLoading(false);
    }
  }

  // Load field schedules
  Future<void> loadFieldSchedules() async {
    try {
      _setLoading(true);
      _clearError();

      final schedules = await _apiService.getSMLFieldSchedules(
        page: 1,
        pageSize: 100,
        sortBy: 'scheduled_date',
        sortOrder: 'asc',
      );

      _fieldSchedules = schedules;
    } catch (e) {
      _setError(e.toString());
    } finally {
      _setLoading(false);
    }
  }

  // Search field visits
  Future<void> searchFieldVisits(String query) async {
    _searchQuery = query;
    await loadFieldVisits(refresh: true);
  }

  // Filter field visits by status
  Future<void> filterFieldVisitsByStatus(String status) async {
    _statusFilter = status;
    await loadFieldVisits(refresh: true);
  }

  // Filter field visits by priority
  Future<void> filterFieldVisitsByPriority(String priority) async {
    _priorityFilter = priority;
    await loadFieldVisits(refresh: true);
  }

  // Get single field visit
  Future<SMLFieldVisit?> getFieldVisit(int visitId) async {
    try {
      _setLoading(true);
      _clearError();
      
      final visit = await _apiService.getSMLFieldVisit(visitId);
      _selectedVisit = visit;
      return visit;
    } catch (e) {
      _setError(e.toString());
      return null;
    } finally {
      _setLoading(false);
    }
  }

  // Create new field visit
  Future<bool> createFieldVisit(SMLFieldVisit visit) async {
    try {
      _setLoading(true);
      _clearError();
      
      final newVisit = await _apiService.createSMLFieldVisit(visit);
      _fieldVisits.insert(0, newVisit);
      notifyListeners();
      return true;
    } catch (e) {
      _setError(e.toString());
      return false;
    } finally {
      _setLoading(false);
    }
  }

  // Update field visit
  Future<bool> updateFieldVisit(int visitId, SMLFieldVisit visit) async {
    try {
      _setLoading(true);
      _clearError();
      
      final updatedVisit = await _apiService.updateSMLFieldVisit(visitId, visit);
      
      final index = _fieldVisits.indexWhere((v) => v.id == visitId);
      if (index != -1) {
        _fieldVisits[index] = updatedVisit;
      }
      
      if (_selectedVisit?.id == visitId) {
        _selectedVisit = updatedVisit;
      }
      
      notifyListeners();
      return true;
    } catch (e) {
      _setError(e.toString());
      return false;
    } finally {
      _setLoading(false);
    }
  }

  // Delete field visit
  Future<bool> deleteFieldVisit(int visitId) async {
    try {
      _setLoading(true);
      _clearError();
      
      await _apiService.deleteSMLFieldVisit(visitId);
      
      _fieldVisits.removeWhere((v) => v.id == visitId);
      if (_selectedVisit?.id == visitId) {
        _selectedVisit = null;
      }
      
      notifyListeners();
      return true;
    } catch (e) {
      _setError(e.toString());
      return false;
    } finally {
      _setLoading(false);
    }
  }

  // Select field visit
  void selectFieldVisit(SMLFieldVisit? visit) {
    _selectedVisit = visit;
    notifyListeners();
  }

  // Select field schedule
  void selectFieldSchedule(SMLFieldSchedule? schedule) {
    _selectedSchedule = schedule;
    notifyListeners();
  }

  // Clear error
  void clearError() {
    _errorMessage = null;
    notifyListeners();
  }

  // Private methods
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
  }
}

// SML Reports Provider
class SMLReportsProvider extends ChangeNotifier {
  final SMLApiService _apiService = SMLApiService();
  
  Map<String, dynamic> _dashboardStats = {};
  Map<String, dynamic> _analytics = {};
  List<Map<String, dynamic>> _reports = [];
  bool _isLoading = false;
  String? _errorMessage;

  // Getters
  Map<String, dynamic> get dashboardStats => _dashboardStats;
  Map<String, dynamic> get analytics => _analytics;
  List<Map<String, dynamic>> get reports => _reports;
  bool get isLoading => _isLoading;
  String? get errorMessage => _errorMessage;

  // Load dashboard stats
  Future<void> loadDashboardStats() async {
    try {
      _setLoading(true);
      _clearError();

      final stats = await _apiService.getSMLDashboardStats();
      _dashboardStats = stats;
    } catch (e) {
      _setError(e.toString());
    } finally {
      _setLoading(false);
    }
  }

  // Load analytics
  Future<void> loadAnalytics({
    String? period,
    String? type,
    String? groupBy,
  }) async {
    try {
      _setLoading(true);
      _clearError();

      final analyticsData = await _apiService.getSMLAnalytics(
        period: period,
        type: type,
        groupBy: groupBy,
      );
      _analytics = analyticsData;
    } catch (e) {
      _setError(e.toString());
    } finally {
      _setLoading(false);
    }
  }

  // Load reports
  Future<void> loadReports({
    String? reportType,
    String? status,
    String? dateFrom,
    String? dateTo,
  }) async {
    try {
      _setLoading(true);
      _clearError();

      final reportsData = await _apiService.getSMLReports(
        reportType: reportType,
        status: status,
        dateFrom: dateFrom,
        dateTo: dateTo,
      );
      _reports = reportsData;
    } catch (e) {
      _setError(e.toString());
    } finally {
      _setLoading(false);
    }
  }

  // Clear error
  void clearError() {
    _errorMessage = null;
    notifyListeners();
  }

  // Private methods
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
  }
}

