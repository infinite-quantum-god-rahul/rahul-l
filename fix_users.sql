-- Fix corrupted user_id data in companies_users table
-- This script sets invalid user_id values to NULL

-- First, check what corrupted data exists
SELECT id, user_id FROM companies_users WHERE user_id NOT REGEXP '^[0-9]+$' AND user_id IS NOT NULL;

-- Fix the corrupted data by setting user_id to NULL
UPDATE companies_users SET user_id = NULL WHERE user_id NOT REGEXP '^[0-9]+$' AND user_id IS NOT NULL;

-- Verify the fix
SELECT COUNT(*) as remaining_corrupted FROM companies_users WHERE user_id NOT REGEXP '^[0-9]+$' AND user_id IS NOT NULL;
