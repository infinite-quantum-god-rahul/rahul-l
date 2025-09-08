class User {
  final int id;
  final String username;
  final String email;
  final String firstName;
  final String lastName;
  final String? phoneNumber;
  final String? profilePicture;
  final String role;
  final List<String> permissions;
  final bool isActive;
  final bool isStaff;
  final bool isSuperuser;
  final DateTime createdAt;
  final DateTime? lastLogin;
  final Map<String, dynamic>? additionalData;
  
  User({
    required this.id,
    required this.username,
    required this.email,
    required this.firstName,
    required this.lastName,
    this.phoneNumber,
    this.profilePicture,
    required this.role,
    required this.permissions,
    required this.isActive,
    required this.isStaff,
    required this.isSuperuser,
    required this.createdAt,
    this.lastLogin,
    this.additionalData,
  });
  
  // Getter for full name
  String get fullName => '$firstName $lastName';
  
  // Getter for display name
  String get displayName => firstName.isNotEmpty ? fullName : username;
  
  // Getter for initials
  String get initials {
    if (firstName.isNotEmpty && lastName.isNotEmpty) {
      return '${firstName[0]}${lastName[0]}'.toUpperCase();
    } else if (firstName.isNotEmpty) {
      return firstName[0].toUpperCase();
    } else if (username.isNotEmpty) {
      return username[0].toUpperCase();
    }
    return 'U';
  }
  
  // Check if user has specific permission
  bool hasPermission(String permission) {
    return permissions.contains(permission);
  }
  
  // Check if user has any of the specified permissions
  bool hasAnyPermission(List<String> permissionList) {
    return permissionList.any((permission) => permissions.contains(permission));
  }
  
  // Check if user has all of the specified permissions
  bool hasAllPermissions(List<String> permissionList) {
    return permissionList.every((permission) => permissions.contains(permission));
  }
  
  // Check if user is admin
  bool get isAdmin => isSuperuser || role == 'admin';
  
  // Check if user is staff member
  bool get isStaffMember => isStaff || isSuperuser;
  
  // Check if user can manage clients
  bool get canManageClients => hasPermission('client_management') || isAdmin;
  
  // Check if user can manage loans
  bool get canManageLoans => hasPermission('loan_management') || isAdmin;
  
  // Check if user can manage field operations
  bool get canManageFieldOperations => hasPermission('field_operations') || isAdmin;
  
  // Check if user can view reports
  bool get canViewReports => hasPermission('view_reports') || isAdmin;
  
  // Check if user can manage users
  bool get canManageUsers => hasPermission('user_management') || isAdmin;
  
  // Check if user can manage settings
  bool get canManageSettings => hasPermission('settings_management') || isAdmin;
  
  // Factory constructor from JSON
  factory User.fromJson(Map<String, dynamic> json) {
    return User(
      id: json['id'] ?? 0,
      username: json['username'] ?? '',
      email: json['email'] ?? '',
      firstName: json['first_name'] ?? json['firstName'] ?? '',
      lastName: json['last_name'] ?? json['lastName'] ?? '',
      phoneNumber: json['phone_number'] ?? json['phoneNumber'],
      profilePicture: json['profile_picture'] ?? json['profilePicture'],
      role: json['role'] ?? 'user',
      permissions: List<String>.from(json['permissions'] ?? []),
      isActive: json['is_active'] ?? json['isActive'] ?? true,
      isStaff: json['is_staff'] ?? json['isStaff'] ?? false,
      isSuperuser: json['is_superuser'] ?? json['isSuperuser'] ?? false,
      createdAt: json['created_at'] != null 
          ? DateTime.parse(json['created_at']) 
          : json['createdAt'] != null 
              ? DateTime.parse(json['createdAt'])
              : DateTime.now(),
      lastLogin: json['last_login'] != null 
          ? DateTime.parse(json['last_login'])
          : json['lastLogin'] != null 
              ? DateTime.parse(json['lastLogin'])
              : null,
      additionalData: json['additional_data'] ?? json['additionalData'],
    );
  }
  
  // Convert to JSON
  Map<String, dynamic> toJson() {
    return {
      'id': id,
      'username': username,
      'email': email,
      'first_name': firstName,
      'last_name': lastName,
      'phone_number': phoneNumber,
      'profile_picture': profilePicture,
      'role': role,
      'permissions': permissions,
      'is_active': isActive,
      'is_staff': isStaff,
      'is_superuser': isSuperuser,
      'created_at': createdAt.toIso8601String(),
      'last_login': lastLogin?.toIso8601String(),
      'additional_data': additionalData,
    };
  }
  
  // Create a copy with updated fields
  User copyWith({
    int? id,
    String? username,
    String? email,
    String? firstName,
    String? lastName,
    String? phoneNumber,
    String? profilePicture,
    String? role,
    List<String>? permissions,
    bool? isActive,
    bool? isStaff,
    bool? isSuperuser,
    DateTime? createdAt,
    DateTime? lastLogin,
    Map<String, dynamic>? additionalData,
  }) {
    return User(
      id: id ?? this.id,
      username: username ?? this.username,
      email: email ?? this.email,
      firstName: firstName ?? this.firstName,
      lastName: lastName ?? this.lastName,
      phoneNumber: phoneNumber ?? this.phoneNumber,
      profilePicture: profilePicture ?? this.profilePicture,
      role: role ?? this.role,
      permissions: permissions ?? this.permissions,
      isActive: isActive ?? this.isActive,
      isStaff: isStaff ?? this.isStaff,
      isSuperuser: isSuperuser ?? this.isSuperuser,
      createdAt: createdAt ?? this.createdAt,
      lastLogin: lastLogin ?? this.lastLogin,
      additionalData: additionalData ?? this.additionalData,
    );
  }
  
  // Equality operator
  @override
  bool operator ==(Object other) {
    if (identical(this, other)) return true;
    return other is User && other.id == id;
  }
  
  // Hash code
  @override
  int get hashCode => id.hashCode;
  
  // String representation
  @override
  String toString() {
    return 'User(id: $id, username: $username, email: $email, name: $fullName, role: $role)';
  }
  
  // Static methods for common user types
  static User get defaultUser => User(
    id: 0,
    username: 'guest',
    email: 'guest@example.com',
    firstName: 'Guest',
    lastName: 'User',
    role: 'guest',
    permissions: [],
    isActive: false,
    isStaff: false,
    isSuperuser: false,
    createdAt: DateTime.now(),
  );
  
  static User get adminUser => User(
    id: 1,
    username: 'admin',
    email: 'admin@sml.com',
    firstName: 'System',
    lastName: 'Administrator',
    role: 'admin',
    permissions: [
      'user_management',
      'client_management',
      'loan_management',
      'field_operations',
      'view_reports',
      'settings_management',
      'data_export',
      'system_configuration',
    ],
    isActive: true,
    isStaff: true,
    isSuperuser: true,
    createdAt: DateTime.now(),
  );
  
  static User get staffUser => User(
    id: 2,
    username: 'staff',
    email: 'staff@sml.com',
    firstName: 'Staff',
    lastName: 'Member',
    role: 'staff',
    permissions: [
      'client_management',
      'loan_management',
      'field_operations',
      'view_reports',
    ],
    isActive: true,
    isStaff: true,
    isSuperuser: false,
    createdAt: DateTime.now(),
  );
  
  static User get fieldUser => User(
    id: 3,
    username: 'field',
    email: 'field@sml.com',
    firstName: 'Field',
    lastName: 'Agent',
    role: 'field_agent',
    permissions: [
      'field_operations',
      'view_reports',
    ],
    isActive: true,
    isStaff: false,
    isSuperuser: false,
    createdAt: DateTime.now(),
  );
  
  // Permission constants
  static const String permissionUserManagement = 'user_management';
  static const String permissionClientManagement = 'client_management';
  static const String permissionLoanManagement = 'loan_management';
  static const String permissionFieldOperations = 'field_operations';
  static const String permissionViewReports = 'view_reports';
  static const String permissionSettingsManagement = 'settings_management';
  static const String permissionDataExport = 'data_export';
  static const String permissionSystemConfiguration = 'system_configuration';
  
  // Role constants
  static const String roleAdmin = 'admin';
  static const String roleStaff = 'staff';
  static const String roleFieldAgent = 'field_agent';
  static const String roleUser = 'user';
  static const String roleGuest = 'guest';
  
  // Get role display name
  String get roleDisplayName {
    switch (role.toLowerCase()) {
      case roleAdmin:
        return 'Administrator';
      case roleStaff:
        return 'Staff Member';
      case roleFieldAgent:
        return 'Field Agent';
      case roleUser:
        return 'User';
      case roleGuest:
        return 'Guest';
      default:
        return role;
    }
  }
  
  // Get role color (for UI)
  int get roleColor {
    switch (role.toLowerCase()) {
      case roleAdmin:
        return 0xFFD32F2F; // Red
      case roleStaff:
        return 0xFF1976D2; // Blue
      case roleFieldAgent:
        return 0xFF388E3C; // Green
      case roleUser:
        return 0xFF757575; // Gray
      case roleGuest:
        return 0xFF9E9E9E; // Light Gray
      default:
        return 0xFF757575; // Default Gray
    }
  }
  
  // Check if user can perform action
  bool canPerformAction(String action) {
    switch (action) {
      case 'create_client':
        return canManageClients;
      case 'edit_client':
        return canManageClients;
      case 'delete_client':
        return canManageClients;
      case 'create_loan':
        return canManageLoans;
      case 'edit_loan':
        return canManageLoans;
      case 'approve_loan':
        return canManageLoans;
      case 'create_field_visit':
        return canManageFieldOperations;
      case 'edit_field_visit':
        return canManageFieldOperations;
      case 'view_analytics':
        return canViewReports;
      case 'export_data':
        return hasPermission(permissionDataExport) || isAdmin;
      case 'manage_users':
        return canManageUsers;
      case 'manage_settings':
        return canManageSettings;
      default:
        return false;
    }
  }
}

