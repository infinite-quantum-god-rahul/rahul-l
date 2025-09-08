// App Constants
class AppConstants {
  // App Information
  static const String appName = 'SML Professional';
  static const String appVersion = '1.0.0';
  static const String appBuildNumber = '1';
  
  // Company Information
  static const String companyName = 'Spoorthi MACS Ltd.';
  static const String companyTagline = 'Professional Loan Management';
  static const String companyWebsite = 'https://www.sml.com';
  static const String companyEmail = 'support@sml.com';
  static const String companyPhone = '+91-XXXXXXXXXX';
  
  // API Endpoints
  static const String apiBaseUrl = 'http://127.0.0.1:8000/api/';
  static const String apiVersion = 'v1';
  
  // Authentication
  static const String authTokenKey = 'auth_token';
  static const String refreshTokenKey = 'refresh_token';
  static const String userDataKey = 'user_data';
  static const String biometricEnabledKey = 'biometric_enabled';
  
  // Storage Keys
  static const String themeKey = 'app_theme';
  static const String languageKey = 'app_language';
  static const String countryKey = 'app_country';
  static const String notificationsKey = 'notifications_enabled';
  static const String autoSyncKey = 'auto_sync_enabled';
  static const String offlineModeKey = 'offline_mode_enabled';
  
  // Database
  static const String hiveBoxName = 'sml_professional';
  static const String userBoxName = 'users';
  static const String clientBoxName = 'clients';
  static const String loanBoxName = 'loans';
  static const String fieldBoxName = 'field_operations';
  static const String reportBoxName = 'reports';
  static const String cacheBoxName = 'cache';
  
  // File Storage
  static const String documentsPath = '/documents';
  static const String imagesPath = '/images';
  static const String tempPath = '/temp';
  static const String cachePath = '/cache';
  static const String backupPath = '/backup';
  
  // File Types
  static const List<String> allowedImageTypes = ['jpg', 'jpeg', 'png', 'gif', 'webp'];
  static const List<String> allowedDocumentTypes = ['pdf', 'doc', 'docx', 'xls', 'xlsx'];
  static const List<String> allowedVideoTypes = ['mp4', 'avi', 'mov', 'mkv'];
  static const List<String> allowedAudioTypes = ['mp3', 'wav', 'aac', 'ogg'];
  
  // File Size Limits
  static const int maxImageSize = 5 * 1024 * 1024; // 5MB
  static const int maxDocumentSize = 10 * 1024 * 1024; // 10MB
  static const int maxVideoSize = 50 * 1024 * 1024; // 50MB
  static const int maxAudioSize = 10 * 1024 * 1024; // 10MB
  
  // Time Constants
  static const int sessionTimeout = 3600000; // 1 hour in milliseconds
  static const int autoLogoutDelay = 300000; // 5 minutes in milliseconds
  static const int syncInterval = 300000; // 5 minutes in milliseconds
  static const int cacheExpiry = 86400000; // 24 hours in milliseconds
  
  // UI Constants
  static const double defaultPadding = 16.0;
  static const double defaultMargin = 16.0;
  static const double defaultRadius = 8.0;
  static const double defaultElevation = 2.0;
  static const double defaultIconSize = 24.0;
  static const double defaultButtonHeight = 48.0;
  static const double defaultInputHeight = 56.0;
  
  // Animation Durations
  static const Duration fastAnimation = Duration(milliseconds: 200);
  static const Duration normalAnimation = Duration(milliseconds: 300);
  static const Duration slowAnimation = Duration(milliseconds: 500);
  static const Duration splashAnimation = Duration(milliseconds: 2000);
  
  // Pagination
  static const int defaultPageSize = 20;
  static const int maxPageSize = 100;
  static const int minPageSize = 10;
  
  // Search
  static const int searchDebounceDelay = 500; // milliseconds
  static const int minSearchLength = 2;
  static const int maxSearchLength = 100;
  
  // Validation
  static const int minPasswordLength = 8;
  static const int maxPasswordLength = 128;
  static const int minUsernameLength = 3;
  static const int maxUsernameLength = 30;
  static const int minNameLength = 2;
  static const int maxNameLength = 50;
  static const int maxPhoneLength = 15;
  static const int maxAddressLength = 200;
  
  // Error Messages
  static const String networkError = 'No internet connection. Please check your network settings.';
  static const String serverError = 'Server error. Please try again later.';
  static const String timeoutError = 'Request timeout. Please try again.';
  static const String unauthorizedError = 'Unauthorized. Please login again.';
  static const String forbiddenError = 'Access denied. You don\'t have permission.';
  static const String notFoundError = 'Resource not found.';
  static const String validationError = 'Please check your input and try again.';
  static const String unknownError = 'An unexpected error occurred. Please try again.';
  
  // Success Messages
  static const String loginSuccess = 'Login successful!';
  static const String logoutSuccess = 'Logout successful!';
  static const String profileUpdateSuccess = 'Profile updated successfully!';
  static const String passwordChangeSuccess = 'Password changed successfully!';
  static const String dataSavedSuccess = 'Data saved successfully!';
  static const String dataDeletedSuccess = 'Data deleted successfully!';
  static const String syncSuccess = 'Data synchronized successfully!';
  
  // Info Messages
  static const String noDataAvailable = 'No data available.';
  static const String loadingData = 'Loading data...';
  static const String savingData = 'Saving data...';
  static const String syncingData = 'Synchronizing data...';
  static const String processingRequest = 'Processing your request...';
  static const String pleaseWait = 'Please wait...';
  
  // Warning Messages
  static const String unsavedChanges = 'You have unsaved changes. Are you sure you want to leave?';
  static const String deleteConfirmation = 'Are you sure you want to delete this item?';
  static const String logoutConfirmation = 'Are you sure you want to logout?';
  static const String dataLossWarning = 'This action may result in data loss. Continue?';
  
  // Form Labels
  static const String usernameLabel = 'Username';
  static const String passwordLabel = 'Password';
  static const String confirmPasswordLabel = 'Confirm Password';
  static const String currentPasswordLabel = 'Current Password';
  static const String newPasswordLabel = 'New Password';
  static const String emailLabel = 'Email';
  static const String phoneLabel = 'Phone Number';
  static const String firstNameLabel = 'First Name';
  static const String lastNameLabel = 'Last Name';
  static const String fullNameLabel = 'Full Name';
  static const String addressLabel = 'Address';
  static const String cityLabel = 'City';
  static const String stateLabel = 'State';
  static const String countryLabel = 'Country';
  static const String pincodeLabel = 'Pincode';
  
  // Form Hints
  static const String usernameHint = 'Enter your username';
  static const String passwordHint = 'Enter your password';
  static const String confirmPasswordHint = 'Confirm your password';
  static const String currentPasswordHint = 'Enter your current password';
  static const String newPasswordHint = 'Enter your new password';
  static const String emailHint = 'Enter your email address';
  static const String phoneHint = 'Enter your phone number';
  static const String firstNameHint = 'Enter your first name';
  static const String lastNameHint = 'Enter your last name';
  static const String fullNameHint = 'Enter your full name';
  static const String addressHint = 'Enter your address';
  static const String cityHint = 'Enter your city';
  static const String stateHint = 'Enter your state';
  static const String countryHint = 'Enter your country';
  static const String pincodeHint = 'Enter your pincode';
  
  // Button Text
  static const String loginButton = 'Login';
  static const String logoutButton = 'Logout';
  static const String registerButton = 'Register';
  static const String submitButton = 'Submit';
  static const String saveButton = 'Save';
  static const String updateButton = 'Update';
  static const String deleteButton = 'Delete';
  static const String cancelButton = 'Cancel';
  static const String confirmButton = 'Confirm';
  static const String yesButton = 'Yes';
  static const String noButton = 'No';
  static const String okButton = 'OK';
  static const String closeButton = 'Close';
  static const String backButton = 'Back';
  static const String nextButton = 'Next';
  static const String previousButton = 'Previous';
  static const String finishButton = 'Finish';
  static const String retryButton = 'Retry';
  static const String refreshButton = 'Refresh';
  static const String syncButton = 'Sync';
  static const String exportButton = 'Export';
  static const String importButton = 'Import';
  static const String searchButton = 'Search';
  static const String filterButton = 'Filter';
  static const String sortButton = 'Sort';
  static const String clearButton = 'Clear';
  static const String resetButton = 'Reset';
  
  // Tab Labels
  static const String dashboardTab = 'Dashboard';
  static const String clientsTab = 'Clients';
  static const String loansTab = 'Loans';
  static const String fieldTab = 'Field';
  static const String reportsTab = 'Reports';
  static const String profileTab = 'Profile';
  
  // Menu Items
  static const String homeMenu = 'Home';
  static const String dashboardMenu = 'Dashboard';
  static const String clientsMenu = 'Clients';
  static const String loansMenu = 'Loans';
  static const String fieldMenu = 'Field Operations';
  static const String reportsMenu = 'Reports';
  static const String analyticsMenu = 'Analytics';
  static const String profileMenu = 'Profile';
  static const String settingsMenu = 'Settings';
  static const String helpMenu = 'Help & Support';
  static const String aboutMenu = 'About';
  static const String logoutMenu = 'Logout';
  
  // Status Values
  static const String statusActive = 'active';
  static const String statusInactive = 'inactive';
  static const String statusPending = 'pending';
  static const String statusApproved = 'approved';
  static const String statusRejected = 'rejected';
  static const String statusProcessing = 'processing';
  static const String statusCompleted = 'completed';
  static const String statusCancelled = 'cancelled';
  static const String statusDraft = 'draft';
  static const String statusSubmitted = 'submitted';
  static const String statusUnderReview = 'under_review';
  static const String statusOnHold = 'on_hold';
  
  // Priority Values
  static const String priorityLow = 'low';
  static const String priorityMedium = 'medium';
  static const String priorityHigh = 'high';
  static const String priorityCritical = 'critical';
  static const String priorityUrgent = 'urgent';
  
  // Loan Types
  static const String loanTypePersonal = 'personal';
  static const String loanTypeBusiness = 'business';
  static const String loanTypeHome = 'home';
  static const String loanTypeVehicle = 'vehicle';
  static const String loanTypeEducation = 'education';
  static const String loanTypeAgriculture = 'agriculture';
  static const String loanTypeMicrofinance = 'microfinance';
  
  // Client Types
  static const String clientTypeIndividual = 'individual';
  static const String clientTypeBusiness = 'business';
  static const String clientTypeGroup = 'group';
  static const String clientTypeCorporate = 'corporate';
  
  // Document Types
  static const String documentTypeAadhaar = 'aadhaar';
  static const String documentTypePAN = 'pan';
  static const String documentTypePassport = 'passport';
  static const String documentTypeDrivingLicense = 'driving_license';
  static const String documentTypeVoterID = 'voter_id';
  static const String documentTypeIncomeProof = 'income_proof';
  static const String documentTypeAddressProof = 'address_proof';
  static const String documentTypeBankStatement = 'bank_statement';
  static const String documentTypeSalarySlip = 'salary_slip';
  static const String documentTypeBusinessProof = 'business_proof';
  
  // Field Visit Types
  static const String visitTypeClientMeeting = 'client_meeting';
  static const String visitTypeDocumentCollection = 'document_collection';
  static const String visitTypeSiteInspection = 'site_inspection';
  static const String visitTypePaymentCollection = 'payment_collection';
  static const String visitTypeFollowUp = 'follow_up';
  static const String visitTypeSurvey = 'survey';
  
  // Report Types
  static const String reportTypeLoanSummary = 'loan_summary';
  static const String reportTypeClientSummary = 'client_summary';
  static const String reportTypeCollectionSummary = 'collection_summary';
  static const String reportTypeNPASummary = 'npa_summary';
  static const String reportTypeFieldSummary = 'field_summary';
  static const String reportTypePerformanceSummary = 'performance_summary';
  static const String reportTypeFinancialSummary = 'financial_summary';
  
  // Export Formats
  static const String exportFormatPDF = 'pdf';
  static const String exportFormatExcel = 'excel';
  static const String exportFormatCSV = 'csv';
  static const String exportFormatJSON = 'json';
  
  // Time Periods
  static const String periodToday = 'today';
  static const String periodYesterday = 'yesterday';
  static const String periodThisWeek = 'this_week';
  static const String periodLastWeek = 'last_week';
  static const String periodThisMonth = 'this_month';
  static const String periodLastMonth = 'last_month';
  static const String periodThisQuarter = 'this_quarter';
  static const String periodLastQuarter = 'last_quarter';
  static const String periodThisYear = 'this_year';
  static const String periodLastYear = 'last_year';
  static const String periodCustom = 'custom';
  
  // Currency
  static const String defaultCurrency = 'INR';
  static const String currencySymbol = '₹';
  
  // Date Formats
  static const String dateFormatDisplay = 'dd MMM yyyy';
  static const String dateFormatAPI = 'yyyy-MM-dd';
  static const String dateFormatDatabase = 'yyyy-MM-dd HH:mm:ss';
  static const String dateFormatShort = 'dd/MM/yyyy';
  static const String dateFormatLong = 'EEEE, dd MMMM yyyy';
  
  // Time Formats
  static const String timeFormatDisplay = 'hh:mm a';
  static const String timeFormatAPI = 'HH:mm:ss';
  static const String timeFormat24Hour = 'HH:mm';
  
  // Regex Patterns
  static const String emailPattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,
  // Missing constants
  static const String pinKey = 'pin_key';
  static const String pinEnabledKey = 'pin_enabled_key';
  static const String useSystemThemeKey = 'use_system_theme_key';
  static const String useHighContrastKey = 'use_high_contrast_key';
  static const String useLargeTextKey = 'use_large_text_key';
  static const String useReducedMotionKey = 'use_reduced_motion_key';
  static const String fontScaleKey = 'font_scale_key';
  static const String themeModeKey = 'theme_mode_key';
  static const String accentColorKey = 'accent_color_key';
  static const String fontFamilyKey = 'font_family_key';
  static const String emailPattern = r'^[^@]+@[^@]+\.[^@]+$';
  static const String phonePattern = r'^\+?[\d\s\-\(\)]+$';
  static const int minPasswordLength = 8;
  static const String addClient = '/add-client';
  static const String newLoan = '/new-loan';
  static const String addFieldVisit = '/add-field-visit';
  static const String loanSchedule = '/loan-schedule';
  static const String payment = '/payment';
  static const String loanAnalytics = '/loan-analytics';
  static const String mapView = '/map-view';
  static const String photoCapture = '/photo-capture';
  static const String notifications = '/notifications';
  static const String activities = '/activities';

}$';
  static const String phonePattern = r'^[0-9+\-\s()]{10,15
  // Missing constants
  static const String pinKey = 'pin_key';
  static const String pinEnabledKey = 'pin_enabled_key';
  static const String useSystemThemeKey = 'use_system_theme_key';
  static const String useHighContrastKey = 'use_high_contrast_key';
  static const String useLargeTextKey = 'use_large_text_key';
  static const String useReducedMotionKey = 'use_reduced_motion_key';
  static const String fontScaleKey = 'font_scale_key';
  static const String themeModeKey = 'theme_mode_key';
  static const String accentColorKey = 'accent_color_key';
  static const String fontFamilyKey = 'font_family_key';
  static const String emailPattern = r'^[^@]+@[^@]+\.[^@]+$';
  static const String phonePattern = r'^\+?[\d\s\-\(\)]+$';
  static const int minPasswordLength = 8;
  static const String addClient = '/add-client';
  static const String newLoan = '/new-loan';
  static const String addFieldVisit = '/add-field-visit';
  static const String loanSchedule = '/loan-schedule';
  static const String payment = '/payment';
  static const String loanAnalytics = '/loan-analytics';
  static const String mapView = '/map-view';
  static const String photoCapture = '/photo-capture';
  static const String notifications = '/notifications';
  static const String activities = '/activities';

}$';
  static const String pincodePattern = r'^[0-9]{6
  // Missing constants
  static const String pinKey = 'pin_key';
  static const String pinEnabledKey = 'pin_enabled_key';
  static const String useSystemThemeKey = 'use_system_theme_key';
  static const String useHighContrastKey = 'use_high_contrast_key';
  static const String useLargeTextKey = 'use_large_text_key';
  static const String useReducedMotionKey = 'use_reduced_motion_key';
  static const String fontScaleKey = 'font_scale_key';
  static const String themeModeKey = 'theme_mode_key';
  static const String accentColorKey = 'accent_color_key';
  static const String fontFamilyKey = 'font_family_key';
  static const String emailPattern = r'^[^@]+@[^@]+\.[^@]+$';
  static const String phonePattern = r'^\+?[\d\s\-\(\)]+$';
  static const int minPasswordLength = 8;
  static const String addClient = '/add-client';
  static const String newLoan = '/new-loan';
  static const String addFieldVisit = '/add-field-visit';
  static const String loanSchedule = '/loan-schedule';
  static const String payment = '/payment';
  static const String loanAnalytics = '/loan-analytics';
  static const String mapView = '/map-view';
  static const String photoCapture = '/photo-capture';
  static const String notifications = '/notifications';
  static const String activities = '/activities';

}$';
  static const String aadhaarPattern = r'^[0-9]{12
  // Missing constants
  static const String pinKey = 'pin_key';
  static const String pinEnabledKey = 'pin_enabled_key';
  static const String useSystemThemeKey = 'use_system_theme_key';
  static const String useHighContrastKey = 'use_high_contrast_key';
  static const String useLargeTextKey = 'use_large_text_key';
  static const String useReducedMotionKey = 'use_reduced_motion_key';
  static const String fontScaleKey = 'font_scale_key';
  static const String themeModeKey = 'theme_mode_key';
  static const String accentColorKey = 'accent_color_key';
  static const String fontFamilyKey = 'font_family_key';
  static const String emailPattern = r'^[^@]+@[^@]+\.[^@]+$';
  static const String phonePattern = r'^\+?[\d\s\-\(\)]+$';
  static const int minPasswordLength = 8;
  static const String addClient = '/add-client';
  static const String newLoan = '/new-loan';
  static const String addFieldVisit = '/add-field-visit';
  static const String loanSchedule = '/loan-schedule';
  static const String payment = '/payment';
  static const String loanAnalytics = '/loan-analytics';
  static const String mapView = '/map-view';
  static const String photoCapture = '/photo-capture';
  static const String notifications = '/notifications';
  static const String activities = '/activities';

}$';
  static const String panPattern = r'^[A-Z]{5
  // Missing constants
  static const String pinKey = 'pin_key';
  static const String pinEnabledKey = 'pin_enabled_key';
  static const String useSystemThemeKey = 'use_system_theme_key';
  static const String useHighContrastKey = 'use_high_contrast_key';
  static const String useLargeTextKey = 'use_large_text_key';
  static const String useReducedMotionKey = 'use_reduced_motion_key';
  static const String fontScaleKey = 'font_scale_key';
  static const String themeModeKey = 'theme_mode_key';
  static const String accentColorKey = 'accent_color_key';
  static const String fontFamilyKey = 'font_family_key';
  static const String emailPattern = r'^[^@]+@[^@]+\.[^@]+$';
  static const String phonePattern = r'^\+?[\d\s\-\(\)]+$';
  static const int minPasswordLength = 8;
  static const String addClient = '/add-client';
  static const String newLoan = '/new-loan';
  static const String addFieldVisit = '/add-field-visit';
  static const String loanSchedule = '/loan-schedule';
  static const String payment = '/payment';
  static const String loanAnalytics = '/loan-analytics';
  static const String mapView = '/map-view';
  static const String photoCapture = '/photo-capture';
  static const String notifications = '/notifications';
  static const String activities = '/activities';

}[0-9]{4
  // Missing constants
  static const String pinKey = 'pin_key';
  static const String pinEnabledKey = 'pin_enabled_key';
  static const String useSystemThemeKey = 'use_system_theme_key';
  static const String useHighContrastKey = 'use_high_contrast_key';
  static const String useLargeTextKey = 'use_large_text_key';
  static const String useReducedMotionKey = 'use_reduced_motion_key';
  static const String fontScaleKey = 'font_scale_key';
  static const String themeModeKey = 'theme_mode_key';
  static const String accentColorKey = 'accent_color_key';
  static const String fontFamilyKey = 'font_family_key';
  static const String emailPattern = r'^[^@]+@[^@]+\.[^@]+$';
  static const String phonePattern = r'^\+?[\d\s\-\(\)]+$';
  static const int minPasswordLength = 8;
  static const String addClient = '/add-client';
  static const String newLoan = '/new-loan';
  static const String addFieldVisit = '/add-field-visit';
  static const String loanSchedule = '/loan-schedule';
  static const String payment = '/payment';
  static const String loanAnalytics = '/loan-analytics';
  static const String mapView = '/map-view';
  static const String photoCapture = '/photo-capture';
  static const String notifications = '/notifications';
  static const String activities = '/activities';

}[A-Z]{1
  // Missing constants
  static const String pinKey = 'pin_key';
  static const String pinEnabledKey = 'pin_enabled_key';
  static const String useSystemThemeKey = 'use_system_theme_key';
  static const String useHighContrastKey = 'use_high_contrast_key';
  static const String useLargeTextKey = 'use_large_text_key';
  static const String useReducedMotionKey = 'use_reduced_motion_key';
  static const String fontScaleKey = 'font_scale_key';
  static const String themeModeKey = 'theme_mode_key';
  static const String accentColorKey = 'accent_color_key';
  static const String fontFamilyKey = 'font_family_key';
  static const String emailPattern = r'^[^@]+@[^@]+\.[^@]+$';
  static const String phonePattern = r'^\+?[\d\s\-\(\)]+$';
  static const int minPasswordLength = 8;
  static const String addClient = '/add-client';
  static const String newLoan = '/new-loan';
  static const String addFieldVisit = '/add-field-visit';
  static const String loanSchedule = '/loan-schedule';
  static const String payment = '/payment';
  static const String loanAnalytics = '/loan-analytics';
  static const String mapView = '/map-view';
  static const String photoCapture = '/photo-capture';
  static const String notifications = '/notifications';
  static const String activities = '/activities';

}$';
  
  // Default Values
  static const String defaultLanguage = 'en';
  static const String defaultCountry = 'IN';
  static const String defaultTheme = 'light';
  static const bool defaultNotifications = true;
  static const bool defaultAutoSync = true;
  static const bool defaultOfflineMode = false;
  
  // Limits
  static const int maxRetryAttempts = 3;
  static const int maxConcurrentRequests = 5;
  static const int maxOfflineDataAge = 7; // days
  static const int maxCacheSize = 100; // MB
  static const int maxLogEntries = 1000;
  static const int maxSearchHistory = 50;
  
  // Delays
  static const int splashDelay = 2000; // milliseconds
  static const int toastDuration = 3000; // milliseconds
  static const int snackbarDuration = 4000; // milliseconds
  static const int dialogDismissDelay = 100; // milliseconds
  
  // Dimensions
  static const double appBarHeight = 56.0;
  static const double bottomNavHeight = 56.0;
  static const double floatingActionButtonSize = 56.0;
  static const double cardMinHeight = 80.0;
  static const double listTileHeight = 72.0;
  static const double dividerHeight = 1.0;
  static const double chipHeight = 32.0;
  
  // Colors (as integers for easy use)
  static const int primaryColor = 0xFF1976D2;
  static const int secondaryColor = 0xFF4CAF50;
  static const int accentColor = 0xFFFF9800;
  static const int errorColor = 0xFFF44336;
  static const int warningColor = 0xFFFFC107;
  static const int infoColor = 0xFF2196F3;
  static const int successColor = 0xFF4CAF50;
  static const int pendingColor = 0xFFFF9800;
  static const int rejectedColor = 0xFFF44336;
  static const int approvedColor = 0xFF4CAF50;
  static const int processingColor = 0xFF2196F3;
  
  // Icons
  static const String iconDashboard = 'dashboard';
  static const String iconClients = 'people';
  static const String iconLoans = 'account_balance';
  static const String iconField = 'location_on';
  static const String iconReports = 'assessment';
  static const String iconProfile = 'person';
  static const String iconSettings = 'settings';
  static const String iconHelp = 'help';
  static const String iconAbout = 'info';
  static const String iconLogout = 'exit_to_app';
  static const String iconSearch = 'search';
  static const String iconFilter = 'filter_list';
  static const String iconSort = 'sort';
  static const String iconAdd = 'add';
  static const String iconEdit = 'edit';
  static const String iconDelete = 'delete';
  static const String iconView = 'visibility';
  static const String iconDownload = 'download';
  static const String iconUpload = 'upload';
  static const String iconSync = 'sync';
  static const String iconRefresh = 'refresh';
  static const String iconBack = 'arrow_back';
  static const String iconNext = 'arrow_forward';
  static const String iconClose = 'close';
  static const String iconCheck = 'check';
  static const String iconWarning = 'warning';
  static const String iconError = 'error';
  static const String iconInfo = 'info';
  static const String iconSuccess = 'check_circle';
  
  // Localization Keys
  static const String localizationKeyAppName = 'app_name';
  static const String localizationKeyCompanyName = 'company_name';
  static const String localizationKeyCompanyTagline = 'company_tagline';
  static const String localizationKeyLogin = 'login';
  static const String localizationKeyLogout = 'logout';
  static const String localizationKeyDashboard = 'dashboard';
  static const String localizationKeyClients = 'clients';
  static const String localizationKeyLoans = 'loans';
  static const String localizationKeyField = 'field';
  static const String localizationKeyReports = 'reports';
  static const String localizationKeyProfile = 'profile';
  static const String localizationKeySettings = 'settings';
  static const String localizationKeyHelp = 'help';
  static const String localizationKeyAbout = 'about';
  
  // Error Codes
  static const String errorCodeNetwork = 'NETWORK_ERROR';
  static const String errorCodeServer = 'SERVER_ERROR';
  static const String errorCodeTimeout = 'TIMEOUT_ERROR';
  static const String errorCodeUnauthorized = 'UNAUTHORIZED_ERROR';
  static const String errorCodeForbidden = 'FORBIDDEN_ERROR';
  static const String errorCodeNotFound = 'NOT_FOUND_ERROR';
  static const String errorCodeValidation = 'VALIDATION_ERROR';
  static const String errorCodeUnknown = 'UNKNOWN_ERROR';
  
  // Success Codes
  static const String successCodeLogin = 'LOGIN_SUCCESS';
  static const String successCodeLogout = 'LOGOUT_SUCCESS';
  static const String successCodeProfileUpdate = 'PROFILE_UPDATE_SUCCESS';
  static const String successCodePasswordChange = 'PASSWORD_CHANGE_SUCCESS';
  static const String successCodeDataSaved = 'DATA_SAVED_SUCCESS';
  static const String successCodeDataDeleted = 'DATA_DELETED_SUCCESS';
  static const String successCodeSync = 'SYNC_SUCCESS';
  
  // Event Names (for analytics)
  static const String eventAppLaunch = 'app_launch';
  static const String eventAppClose = 'app_close';
  static const String eventLogin = 'login';
  static const String eventLogout = 'logout';
  static const String eventScreenView = 'screen_view';
  static const String eventButtonClick = 'button_click';
  static const String eventFormSubmit = 'form_submit';
  static const String eventDataSync = 'data_sync';
  static const String eventFileUpload = 'file_upload';
  static const String eventFileDownload = 'file_download';
  static const String eventSearch = 'search';
  static const String eventFilter = 'filter';
  static const String eventSort = 'sort';
  static const String eventExport = 'export';
  static const String eventImport = 'import';
  
  // Screen Names (for analytics)
  static const String screenSplash = 'splash';
  static const String screenLogin = 'login';
  static const String screenDashboard = 'dashboard';
  static const String screenClients = 'clients';
  static const String screenClientDetail = 'client_detail';
  static const String screenClientRegistration = 'client_registration';
  static const String screenLoans = 'loans';
  static const String screenLoanDetail = 'loan_detail';
  static const String screenLoanApplication = 'loan_application';
  static const String screenFieldSchedule = 'field_schedule';
  static const String screenFieldVisit = 'field_visit';
  static const String screenReports = 'reports';
  static const String screenAnalytics = 'analytics';
  static const String screenProfile = 'profile';
  static const String screenSettings = 'settings';
  static const String screenHelp = 'help';
  static const String screenAbout = 'about';

  // Missing constants
  static const String pinKey = 'pin_key';
  static const String pinEnabledKey = 'pin_enabled_key';
  static const String useSystemThemeKey = 'use_system_theme_key';
  static const String useHighContrastKey = 'use_high_contrast_key';
  static const String useLargeTextKey = 'use_large_text_key';
  static const String useReducedMotionKey = 'use_reduced_motion_key';
  static const String fontScaleKey = 'font_scale_key';
  static const String themeModeKey = 'theme_mode_key';
  static const String accentColorKey = 'accent_color_key';
  static const String fontFamilyKey = 'font_family_key';
  static const String emailPattern = r'^[^@]+@[^@]+\.[^@]+$';
  static const String phonePattern = r'^\+?[\d\s\-\(\)]+$';
  static const int minPasswordLength = 8;
  static const String addClient = '/add-client';
  static const String newLoan = '/new-loan';
  static const String addFieldVisit = '/add-field-visit';
  static const String loanSchedule = '/loan-schedule';
  static const String payment = '/payment';
  static const String loanAnalytics = '/loan-analytics';
  static const String mapView = '/map-view';
  static const String photoCapture = '/photo-capture';
  static const String notifications = '/notifications';
  static const String activities = '/activities';

}

