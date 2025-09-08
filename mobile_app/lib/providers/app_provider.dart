import 'package:flutter/material.dart';
import 'package:shared_preferences/shared_preferences.dart';
import '../config/app_config.dart';
import '../utils/constants.dart';

class AppProvider extends ChangeNotifier {
  bool _isInitialized = false;
  bool _isLoading = false;
  String _currentLanguage = AppConstants.defaultLanguage;
  String _currentCountry = AppConstants.defaultCountry;
  bool _notificationsEnabled = AppConstants.defaultNotifications;
  bool _autoSyncEnabled = AppConstants.defaultAutoSync;
  bool _offlineModeEnabled = AppConstants.defaultOfflineMode;
  String? _errorMessage;
  String? _successMessage;
  bool _showError = false;
  bool _showSuccess = false;

  // Getters
  bool get isInitialized => _isInitialized;
  bool get isLoading => _isLoading;
  String get currentLanguage => _currentLanguage;
  String get currentCountry => _currentCountry;
  bool get notificationsEnabled => _notificationsEnabled;
  bool get autoSyncEnabled => _autoSyncEnabled;
  bool get offlineModeEnabled => _offlineModeEnabled;
  String? get errorMessage => _errorMessage;
  String? get successMessage => _successMessage;
  bool get showError => _showError;
  bool get showSuccess => _showSuccess;

  // Initialize the app
  Future<void> initialize() async {
    if (_isInitialized) return;

    try {
      _setLoading(true);
      
      // Load saved preferences
      await _loadPreferences();
      
      // Initialize other services
      await _initializeServices();
      
      _isInitialized = true;
      notifyListeners();
    } catch (e) {
      _setError('Failed to initialize app: $e');
    } finally {
      _setLoading(false);
    }
  }

  // Load saved preferences
  Future<void> _loadPreferences() async {
    try {
      final prefs = await SharedPreferences.getInstance();
      
      _currentLanguage = prefs.getString(AppConstants.languageKey) ?? AppConstants.defaultLanguage;
      _currentCountry = prefs.getString(AppConstants.countryKey) ?? AppConstants.defaultCountry;
      _notificationsEnabled = prefs.getBool(AppConstants.notificationsKey) ?? AppConstants.defaultNotifications;
      _autoSyncEnabled = prefs.getBool(AppConstants.autoSyncKey) ?? AppConstants.defaultAutoSync;
      _offlineModeEnabled = prefs.getBool(AppConstants.offlineModeKey) ?? AppConstants.defaultOfflineMode;
    } catch (e) {
      // Use default values if loading fails
      _currentLanguage = AppConstants.defaultLanguage;
      _currentCountry = AppConstants.defaultCountry;
      _notificationsEnabled = AppConstants.defaultNotifications;
      _autoSyncEnabled = AppConstants.defaultAutoSync;
      _offlineModeEnabled = AppConstants.defaultOfflineMode;
    }
  }

  // Initialize services
  Future<void> _initializeServices() async {
    // Initialize API service
    // Initialize database
    // Initialize notifications
    // Initialize analytics
    // Initialize crash reporting
    
    // Simulate initialization delay
    await Future.delayed(const Duration(milliseconds: 500));
  }

  // Change language
  Future<void> changeLanguage(String language) async {
    if (_currentLanguage == language) return;

    try {
      _setLoading(true);
      
      // Validate language
      if (!AppConfig.supportedLanguages.contains(language)) {
        throw Exception('Unsupported language: $language');
      }
      
      // Save preference
      final prefs = await SharedPreferences.getInstance();
      await prefs.setString(AppConstants.languageKey, language);
      
      _currentLanguage = language;
      notifyListeners();
      
      _setSuccess('Language changed to ${_getLanguageDisplayName(language)}');
    } catch (e) {
      _setError('Failed to change language: $e');
    } finally {
      _setLoading(false);
    }
  }

  // Change country
  Future<void> changeCountry(String country) async {
    if (_currentCountry == country) return;

    try {
      _setLoading(true);
      
      // Validate country
      if (!AppConfig.supportedCountries.contains(country)) {
        throw Exception('Unsupported country: $country');
      }
      
      // Save preference
      final prefs = await SharedPreferences.getInstance();
      await prefs.setString(AppConstants.countryKey, country);
      
      _currentCountry = country;
      notifyListeners();
      
      _setSuccess('Country changed to ${_getCountryDisplayName(country)}');
    } catch (e) {
      _setError('Failed to change country: $e');
    } finally {
      _setLoading(false);
    }
  }

  // Toggle notifications
  Future<void> toggleNotifications() async {
    try {
      _setLoading(true);
      
      final newValue = !_notificationsEnabled;
      
      // Save preference
      final prefs = await SharedPreferences.getInstance();
      await prefs.setBool(AppConstants.notificationsKey, newValue);
      
      _notificationsEnabled = newValue;
      notifyListeners();
      
      if (newValue) {
        _setSuccess('Notifications enabled');
      } else {
        _setSuccess('Notifications disabled');
      }
    } catch (e) {
      _setError('Failed to toggle notifications: $e');
    } finally {
      _setLoading(false);
    }
  }

  // Toggle auto sync
  Future<void> toggleAutoSync() async {
    try {
      _setLoading(true);
      
      final newValue = !_autoSyncEnabled;
      
      // Save preference
      final prefs = await SharedPreferences.getInstance();
      await prefs.setBool(AppConstants.autoSyncKey, newValue);
      
      _autoSyncEnabled = newValue;
      notifyListeners();
      
      if (newValue) {
        _setSuccess('Auto sync enabled');
      } else {
        _setSuccess('Auto sync disabled');
      }
    } catch (e) {
      _setError('Failed to toggle auto sync: $e');
    } finally {
      _setLoading(false);
    }
  }

  // Toggle offline mode
  Future<void> toggleOfflineMode() async {
    try {
      _setLoading(true);
      
      final newValue = !_offlineModeEnabled;
      
      // Save preference
      final prefs = await SharedPreferences.getInstance();
      await prefs.setBool(AppConstants.offlineModeKey, newValue);
      
      _offlineModeEnabled = newValue;
      notifyListeners();
      
      if (newValue) {
        _setSuccess('Offline mode enabled');
      } else {
        _setSuccess('Offline mode disabled');
      }
    } catch (e) {
      _setError('Failed to toggle offline mode: $e');
    } finally {
      _setLoading(false);
    }
  }

  // Get language display name
  String _getLanguageDisplayName(String language) {
    switch (language.toLowerCase()) {
      case 'en':
        return 'English';
      case 'hi':
        return 'Hindi';
      case 'kn':
        return 'Kannada';
      default:
        return language;
    }
  }

  // Get country display name
  String _getCountryDisplayName(String country) {
    switch (country.toUpperCase()) {
      case 'IN':
        return 'India';
      default:
        return country;
    }
  }

  // Set loading state
  void _setLoading(bool loading) {
    _isLoading = loading;
    notifyListeners();
  }

  // Set error message
  void _setError(String message) {
    _errorMessage = message;
    _showError = true;
    _showSuccess = false;
    notifyListeners();
    
    // Auto-hide error after 5 seconds
    Future.delayed(const Duration(seconds: 5), () {
      _showError = false;
      notifyListeners();
    });
  }

  // Set success message
  void _setSuccess(String message) {
    _successMessage = message;
    _showSuccess = true;
    _showError = false;
    notifyListeners();
    
    // Auto-hide success after 3 seconds
    Future.delayed(const Duration(seconds: 3), () {
      _showSuccess = false;
      notifyListeners();
    });
  }

  // Clear error message
  void clearError() {
    _showError = false;
    notifyListeners();
  }

  // Clear success message
  void clearSuccess() {
    _showSuccess = false;
    notifyListeners();
  }

  // Clear all messages
  void clearMessages() {
    _showError = false;
    _showSuccess = false;
    notifyListeners();
  }

  // Reset to defaults
  Future<void> resetToDefaults() async {
    try {
      _setLoading(true);
      
      // Reset preferences
      final prefs = await SharedPreferences.getInstance();
      await prefs.remove(AppConstants.languageKey);
      await prefs.remove(AppConstants.countryKey);
      await prefs.remove(AppConstants.notificationsKey);
      await prefs.remove(AppConstants.autoSyncKey);
      await prefs.remove(AppConstants.offlineModeKey);
      
      // Reset to default values
      _currentLanguage = AppConstants.defaultLanguage;
      _currentCountry = AppConstants.defaultCountry;
      _notificationsEnabled = AppConstants.defaultNotifications;
      _autoSyncEnabled = AppConstants.defaultAutoSync;
      _offlineModeEnabled = AppConstants.defaultOfflineMode;
      
      notifyListeners();
      _setSuccess('Settings reset to defaults');
    } catch (e) {
      _setError('Failed to reset settings: $e');
    } finally {
      _setLoading(false);
    }
  }

  // Get app version info
  Map<String, String> getAppVersionInfo() {
    return {
      'version': AppConfig.appVersion,
      'buildNumber': AppConfig.appBuildNumber,
      'appName': AppConfig.appName,
      'companyName': AppConfig.companyName,
    };
  }

  // Check for updates
  Future<bool> checkForUpdates() async {
    try {
      _setLoading(true);
      
      // Simulate update check
      await Future.delayed(const Duration(seconds: 2));
      
      // For now, always return false (no updates)
      return false;
    } catch (e) {
      _setError('Failed to check for updates: $e');
      return false;
    } finally {
      _setLoading(false);
    }
  }

  // Export app data
  Future<bool> exportAppData() async {
    try {
      _setLoading(true);
      
      // Simulate data export
      await Future.delayed(const Duration(seconds: 3));
      
      _setSuccess('App data exported successfully');
      return true;
    } catch (e) {
      _setError('Failed to export app data: $e');
      return false;
    } finally {
      _setLoading(false);
    }
  }

  // Import app data
  Future<bool> importAppData(String filePath) async {
    try {
      _setLoading(true);
      
      // Simulate data import
      await Future.delayed(const Duration(seconds: 3));
      
      _setSuccess('App data imported successfully');
      return true;
    } catch (e) {
      _setError('Failed to import app data: $e');
      return false;
    } finally {
      _setLoading(false);
    }
  }

  // Clear app data
  Future<bool> clearAppData() async {
    try {
      _setLoading(true);
      
      // Simulate data clearing
      await Future.delayed(const Duration(seconds: 2));
      
      _setSuccess('App data cleared successfully');
      return true;
    } catch (e) {
      _setError('Failed to clear app data: $e');
      return false;
    } finally {
      _setLoading(false);
    }
  }

  // Get app statistics
  Map<String, dynamic> getAppStatistics() {
    return {
      'totalClients': 0,
      'totalLoans': 0,
      'totalFieldVisits': 0,
      'totalReports': 0,
      'lastSync': DateTime.now().toIso8601String(),
      'appUptime': '0 days',
      'dataSize': '0 MB',
      'cacheSize': '0 MB',
    };
  }

  // Sync data
  Future<bool> syncData() async {
    try {
      _setLoading(true);
      
      // Simulate data sync
      await Future.delayed(const Duration(seconds: 2));
      
      _setSuccess('Data synchronized successfully');
      return true;
    } catch (e) {
      _setError('Failed to sync data: $e');
      return false;
    } finally {
      _setLoading(false);
    }
  }

  // Backup data
  Future<bool> backupData() async {
    try {
      _setLoading(true);
      
      // Simulate data backup
      await Future.delayed(const Duration(seconds: 3));
      
      _setSuccess('Data backed up successfully');
      return true;
    } catch (e) {
      _setError('Failed to backup data: $e');
      return false;
    } finally {
      _setLoading(false);
    }
  }

  // Restore data
  Future<bool> restoreData(String backupPath) async {
    try {
      _setLoading(true);
      
      // Simulate data restore
      await Future.delayed(const Duration(seconds: 3));
      
      _setSuccess('Data restored successfully');
      return true;
    } catch (e) {
      _setError('Failed to restore data: $e');
      return false;
    } finally {
      _setLoading(false);
    }
  }
}

