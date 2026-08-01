"""Коды ошибок Remnawave API.

Сгенерировано из @remnawave/backend-contract (constants/errors/errors.ts).
Не редактировать вручную — при обновлении контракта перегенерировать.
"""

from enum import StrEnum


class ErrorCode(StrEnum):
    INTERNAL_SERVER_ERROR = "A001"  # 500 — Server error
    LOGIN_ERROR = "A002"  # 500 — Login error
    UNAUTHORIZED = "A003"  # 401 — Unauthorized
    FORBIDDEN_ROLE_ERROR = "A004"  # 403 — Forbidden role error
    CREATE_API_TOKEN_ERROR = "A005"  # 500 — Create API token error
    DELETE_API_TOKEN_ERROR = "A006"  # 500 — Delete API token error
    REQUESTED_TOKEN_NOT_FOUND = "A007"  # 404 — Requested token not found
    FIND_ALL_API_TOKENS_ERROR = "A008"  # 500 — Find all API tokens error
    GET_PUBLIC_KEY_ERROR = "A009"  # 500 — Get public key error
    ENABLE_NODE_ERROR = "A010"  # 500 — Enable node error
    NODE_NOT_FOUND = "A011"  # 404 — Node not found
    CONFIG_NOT_FOUND = "A012"  # 404 — Configuration not found
    UPDATE_CONFIG_ERROR = "A013"  # 500 — Error updating configuration
    GET_CONFIG_ERROR = "A014"  # 500 — Error retrieving configuration
    DELETE_MANY_INBOUNDS_ERROR = "A015"  # 500 — Delete many inbounds error
    CREATE_MANY_INBOUNDS_ERROR = "A016"  # 500 — Create many inbounds error
    FIND_ALL_INBOUNDS_ERROR = "A017"  # 500 — Find all inbounds error
    CREATE_USER_ERROR = "A018"  # 500 — Failed to create user
    USER_USERNAME_ALREADY_EXISTS = "A019"  # 400 — User username already exists
    USER_SHORT_UUID_ALREADY_EXISTS = "A020"  # 400 — User short UUID already exists
    USER_SUBSCRIPTION_UUID_ALREADY_EXISTS = "A021"  # 400 — User subscription UUID already exists
    CREATE_USER_WITH_INBOUNDS_ERROR = "A022"  # 500 — User creation successful, but inbound creation failed. User not created.
    CANT_GET_CREATED_USER_WITH_INBOUNDS = "A023"  # 500 — User creation successful, but failed to get created user with inbounds.
    GET_ALL_USERS_ERROR = "A024"  # 500 — Get all users error
    USER_NOT_FOUND = "A025"  # 404 — User not found
    GET_USER_BY_ERROR = "A026"  # 500 — Get user by error
    REVOKE_USER_SUBSCRIPTION_ERROR = "A027"  # 500 — Revoke user subscription error
    DISABLE_USER_ERROR = "A028"  # 500 — Disable user error
    USER_ALREADY_DISABLED = "A029"  # 400 — User already disabled
    USER_ALREADY_ENABLED = "A030"  # 400 — User already enabled
    ENABLE_USER_ERROR = "A031"  # 500 — Enable user error
    CREATE_NODE_ERROR = "A032"  # 500 — Create node error
    NODE_NAME_ALREADY_EXISTS = "A033"  # 400 — Node name already exists
    NODE_ADDRESS_ALREADY_EXISTS = "A034"  # 400 — Node address already exists
    RESTART_NODE_ERROR = "A035"  # 500 — Restart node error
    GET_CONFIG_WITH_USERS_ERROR = "A036"  # 500 — Get config with users error
    DELETE_USER_ERROR = "A037"  # 500 — Delete user error
    UPDATE_NODE_ERROR = "A038"  # 500 — Update node error
    UPDATE_USER_ERROR = "A039"  # 500 — Update user error
    INCREMENT_USED_TRAFFIC_ERROR = "A040"  # 500 — Increment used traffic error
    GET_ALL_NODES_ERROR = "A041"  # 500 — Get all nodes error
    GET_ONE_NODE_ERROR = "A042"  # 500 — Get one node error
    DELETE_NODE_ERROR = "A043"  # 500 — Delete node error
    CREATE_HOST_ERROR = "A044"  # 500 — Create host error
    HOST_REMARK_ALREADY_EXISTS = "A045"  # 400 — Host remark already exists
    HOST_NOT_FOUND = "A046"  # 404 — Host not found
    DELETE_HOST_ERROR = "A047"  # 500 — Delete host error
    GET_USER_STATS_ERROR = "A048"  # 500 — Get user stats error
    UPDATE_USER_WITH_INBOUNDS_ERROR = "A049"  # 500 — Update user with inbounds error
    GET_ALL_HOSTS_ERROR = "A050"  # 500 — Get all hosts error
    REORDER_HOSTS_ERROR = "A051"  # 500 — Reorder hosts error
    UPDATE_HOST_ERROR = "A052"  # 500 — Update host error
    CREATE_CONFIG_ERROR = "A053"  # 500 — Create config error
    ENABLED_NODES_NOT_FOUND = "A054"  # 409 — Enabled nodes not found
    GET_NODES_USAGE_BY_RANGE_ERROR = "A055"  # 500 — Get nodes usage by range error
    RESET_USER_TRAFFIC_ERROR = "A056"  # 500 — Reset user traffic error
    REORDER_NODES_ERROR = "A057"  # 500 — Reorder nodes error
    GET_ALL_INBOUNDS_ERROR = "A058"  # 500 — Get all inbounds error
    BULK_DELETE_USERS_BY_STATUS_ERROR = "A059"  # 500 — Bulk delete users by status error
    UPDATE_INBOUND_ERROR = "A060"  # 500 — Update inbound error
    CONFIG_VALIDATION_ERROR = "A061"  # 500 — Config validation error
    USERS_NOT_FOUND = "A062"  # 404 — Users not found
    GET_USER_BY_UNIQUE_FIELDS_NOT_FOUND = "A063"  # 404 — User with specified params not found
    UPDATE_EXCEEDED_TRAFFIC_USERS_ERROR = "A064"  # 500 — Update exceeded traffic users error
    ADMIN_NOT_FOUND = "A065"  # 404 — Admin not found
    CREATE_ADMIN_ERROR = "A066"  # 500 — Create admin error
    GET_AUTH_STATUS_ERROR = "A067"  # 500 — Get auth status error
    FORBIDDEN = "A068"  # 403 — Forbidden
    DISABLE_NODE_ERROR = "A069"  # 500 — Disable node error
    GET_ONE_HOST_ERROR = "A070"  # 500 — Get one host error
    SUBSCRIPTION_SETTINGS_NOT_FOUND = "A071"  # 404 — Subscription settings not found
    GET_SUBSCRIPTION_SETTINGS_ERROR = "A072"  # 500 — Get subscription settings error
    UPDATE_SUBSCRIPTION_SETTINGS_ERROR = "A073"  # 500 — Update subscription settings error
    ADD_INBOUND_TO_USERS_ERROR = "A074"  # 500 — Add inbound to users error
    REMOVE_INBOUND_FROM_USERS_ERROR = "A075"  # 500 — Remove inbound from users error
    INBOUND_NOT_FOUND = "A076"  # 404 — Inbound not found
    ADD_INBOUND_TO_NODES_ERROR = "A077"  # 500 — Add inbound to nodes error
    REMOVE_INBOUND_FROM_NODES_ERROR = "A078"  # 500 — Remove inbound from nodes error
    DELETE_HOSTS_ERROR = "A079"  # 500 — Delete hosts error
    BULK_ENABLE_HOSTS_ERROR = "A080"  # 500 — Bulk enable hosts error
    BULK_DISABLE_HOSTS_ERROR = "A081"  # 500 — Bulk disable hosts error
    BULK_DELETE_USERS_BY_UUID_ERROR = "A084"  # 500 — Bulk delete users by UUID error
    BULK_REVOKE_USERS_SUBSCRIPTION_ERROR = "A085"  # 500 — Bulk revoke users subscription error
    BULK_RESET_USER_TRAFFIC_ERROR = "A086"  # 500 — Bulk reset user traffic error
    BULK_UPDATE_USERS_ERROR = "A087"  # 500 — Bulk update users error
    BULK_ADD_INBOUNDS_TO_USERS_ERROR = "A088"  # 500 — Bulk add inbounds to users error
    BULK_UPDATE_ALL_USERS_ERROR = "A089"  # 500 — Bulk update all users error
    INVALID_USER_STATUS_ERROR = "A089"  # 400 — LIMITED and EXPIRED statuses are not allowed to be set manually.
    KEYPAIR_CREATION_ERROR = "A090"  # 500 — Keypair creation error
    GET_USER_USAGE_BY_RANGE_ERROR = "A091"  # 500 — Get user usage by range error
    KEYPAIR_NOT_FOUND = "A092"  # 500 — Keypair not found. Restart app.
    ACTIVATE_ALL_INBOUNDS_ERROR = "A093"  # 500 — Activate all inbounds error
    CREATE_HWID_USER_DEVICE_ERROR = "A096"  # 500 — Create hwid user device error
    CHECK_HWID_EXISTS_ERROR = "A097"  # 500 — Check hwid exists error
    USER_HWID_DEVICE_ALREADY_EXISTS = "A098"  # 400 — User hwid device already exists
    USER_HWID_DEVICE_LIMIT_REACHED = "A099"  # 400 — User hwid device limit reached
    GET_USER_HWID_DEVICES_ERROR = "A100"  # 500 — Get user hwid devices error
    DELETE_HWID_USER_DEVICE_ERROR = "A101"  # 500 — Delete hwid user device error
    UPSERT_HWID_USER_DEVICE_ERROR = "A102"  # 500 — Upsert hwid user device error
    GET_ALL_TAGS_ERROR = "A103"  # 500 — Get all tags error
    GETTING_ALL_SUBSCRIPTIONS_ERROR = "A104"  # 500 — Getting all subscriptions error
    TRIGGER_THRESHOLD_NOTIFICATION_ERROR = "A105"  # 500 — Trigger threshold notification error
    BULK_DELETE_BY_STATUS_ERROR = "A106"  # 500 — Bulk delete by status error
    CLEAN_OLD_USAGE_RECORDS_ERROR = "A107"  # 500 — Clean old usage records error
    VACUUM_TABLE_ERROR = "A108"  # 500 — Vacuum table error
    GET_CONFIG_PROFILES_ERROR = "A109"  # 500 — Get config profiles error
    GET_CONFIG_PROFILE_BY_UUID_ERROR = "A110"  # 500 — Get config profile by UUID error
    CONFIG_PROFILE_NOT_FOUND = "A111"  # 404 — Config profile not found
    CREATE_CONFIG_PROFILE_ERROR = "A112"  # 500 — Create config profile error
    INBOUNDS_WITH_SAME_TAG_ALREADY_EXISTS = "A113"  # 409 — Inbounds with same tag already exists in database. Inbound tags must be unique.
    CONFIG_PROFILE_NAME_ALREADY_EXISTS = "A114"  # 409 — Config profile name already exists in database. Config profile names must be unique.
    GET_INBOUNDS_BY_PROFILE_UUID_ERROR = "A115"  # 500 — Get inbounds by profile UUID error
    GET_INTERNAL_SQUADS_ERROR = "A116"  # 500 — Get internal squads error
    GET_INTERNAL_SQUAD_BY_UUID_ERROR = "A117"  # 500 — Get internal squad by UUID error
    INTERNAL_SQUAD_NOT_FOUND = "A118"  # 404 — Internal squad not found
    CREATE_INTERNAL_SQUAD_ERROR = "A119"  # 500 — Create internal squad error
    INTERNAL_SQUAD_NAME_ALREADY_EXISTS = "A120"  # 409 — Internal squad name already exists
    UPDATE_INTERNAL_SQUAD_ERROR = "A121"  # 500 — Update internal squad error
    DELETE_INTERNAL_SQUAD_ERROR = "A122"  # 500 — Delete internal squad error
    CREATE_USER_WITH_INTERNAL_SQUAD_ERROR = "A123"  # 500 — Create user with internal squad error
    CONFIG_PROFILE_INBOUND_NOT_FOUND_IN_SPECIFIED_PROFILE = "A124"  # 404 — Config profile inbound not found in specified profile
    GET_USER_ACCESSIBLE_NODES_ERROR = "A125"  # 500 — Get user accessible nodes error
    GET_INFRA_PROVIDERS_ERROR = "A126"  # 500 — Get infra providers error
    GET_INFRA_PROVIDER_BY_UUID_ERROR = "A127"  # 500 — Get infra provider by UUID error
    INFRA_PROVIDER_NOT_FOUND = "A128"  # 404 — Infra provider not found
    DELETE_INFRA_PROVIDER_BY_UUID_ERROR = "A129"  # 500 — Delete infra provider by UUID error
    CREATE_INFRA_PROVIDER_ERROR = "A130"  # 500 — Create infra provider error
    UPDATE_INFRA_PROVIDER_ERROR = "A131"  # 500 — Update infra provider error
    CREATE_INFRA_BILLING_HISTORY_RECORD_ERROR = "A132"  # 500 — Create infra billing history record error
    GET_INFRA_BILLING_HISTORY_RECORDS_ERROR = "A133"  # 500 — Get infra billing history records error
    DELETE_INFRA_BILLING_HISTORY_RECORD_BY_UUID_ERROR = "A134"  # 500 — Delete infra billing history record by UUID error
    GET_BILLING_NODES_ERROR = "A135"  # 500 — Get billing nodes error
    UPDATE_INFRA_BILLING_NODE_ERROR = "A136"  # 500 — Update infra billing node error
    CREATE_INFRA_BILLING_NODE_ERROR = "A137"  # 500 — Create infra billing node error
    DELETE_INFRA_BILLING_NODE_BY_UUID_ERROR = "A138"  # 500 — Delete infra billing node by UUID error
    GET_BILLING_NODES_FOR_NOTIFICATIONS_ERROR = "A139"  # 500 — Get billing nodes for notifications error
    ADD_USERS_TO_INTERNAL_SQUAD_ERROR = "A140"  # 500 — Add users to internal squad error
    INTERNAL_SQUAD_BULK_ACTIONS_ERROR = "A141"  # 500 — Internal squad bulk actions error
    REMOVE_USERS_FROM_INTERNAL_SQUAD_ERROR = "A142"  # 500 — Remove users from internal squad error
    DELETE_CONFIG_PROFILE_BY_UUID_ERROR = "A143"  # 500 — Delete config profile by UUID error
    RESERVED_INTERNAL_SQUAD_NAME = "A144"  # 400 — This name is reserved by Remnawave. Please use a different name.
    RESERVED_CONFIG_PROFILE_NAME = "A145"  # 400 — This name is reserved by Remnawave. Please use a different name.
    UPDATE_CONFIG_PROFILE_ERROR = "A146"  # 500 — Update config profile error
    OAUTH2_PROVIDER_NOT_FOUND = "A147"  # 404 — OAuth2 provider not found
    OAUTH2_AUTHORIZE_ERROR = "A148"  # 500 — OAuth2 authorize error
    NODE_IS_DISABLED = "A149"  # 400 — Node is disabled
    SYNC_ACTIVE_PROFILE_ERROR = "A150"  # 500 — Sync active profile error
    GET_ALL_HOST_TAGS_ERROR = "A151"  # 500 — Get all host tags error
    NAME_OR_CONFIG_REQUIRED = "A152"  # 400 — Name or config is required
    NAME_OR_INBOUNDS_REQUIRED = "A153"  # 400 — Name or inbounds is required
    GET_INTERNAL_SQUAD_ACCESSIBLE_NODES_ERROR = "A154"  # 500 — Get internal squad accessible nodes error
    DELETE_HWID_USER_DEVICES_ERROR = "A155"  # 500 — Delete hwid user devices error
    CREATE_USER_SUBSCRIPTION_REQUEST_HISTORY_ERROR = "A156"  # 500 — Create user subscription request history error
    GET_USER_SUBSCRIPTION_REQUEST_HISTORY_ERROR = "A157"  # 500 — Get user subscription request history error
    GET_ALL_HWID_DEVICES_ERROR = "A158"  # 500 — Get all hwid devices error
    GET_HWID_DEVICES_STATS_ERROR = "A159"  # 500 — Get hwid devices stats error
    GET_USER_SUBSCRIPTION_REQUEST_HISTORY_STATS_ERROR = "A160"  # 500 — Get user subscription request history stats error
    GET_SNIPPETS_ERROR = "A161"  # 500 — Get snippets error
    SNIPPET_NOT_FOUND = "A162"  # 404 — Snippet not found
    DELETE_SNIPPET_BY_NAME_ERROR = "A163"  # 500 — Delete snippet by name error
    SNIPPET_NAME_ALREADY_EXISTS = "A164"  # 400 — Snippet name already exists
    UPDATE_SNIPPET_ERROR = "A165"  # 500 — Update snippet error
    SNIPPET_CANNOT_BE_EMPTY = "A166"  # 400 — Snippet cannot be empty
    SNIPPET_CANNOT_CONTAIN_EMPTY_OBJECTS = "A167"  # 400 — Snippet cannot contain empty objects
    GET_ALL_SUBSCRIPTION_TEMPLATES_ERROR = "A168"  # 500 — Get all subscription templates error
    GET_SUBSCRIPTION_TEMPLATE_BY_UUID_ERROR = "A169"  # 500 — Get subscription template by UUID error
    SUBSCRIPTION_TEMPLATE_NOT_FOUND = "A170"  # 404 — Subscription template not found
    UPDATE_SUBSCRIPTION_TEMPLATE_ERROR = "A171"  # 500 — Update subscription template error
    RESERVED_TEMPLATE_NAME = "A172"  # 400 — This name is reserved. Please use a different name.
    TEMPLATE_JSON_NOT_ALLOWED_FOR_YAML_TEMPLATE = "A173"  # 400 — Template JSON is not allowed for YAML template
    TEMPLATE_YAML_NOT_ALLOWED_FOR_JSON_TEMPLATE = "A174"  # 400 — Template YAML is not allowed for JSON template
    TEMPLATE_JSON_AND_YAML_CANNOT_BE_UPDATED_SIMULTANEOUSLY = "A175"  # 400 — Template JSON and YAML cannot be updated simultaneously
    TEMPLATE_NAME_ALREADY_EXISTS_FOR_THIS_TYPE = "A176"  # 400 — Template name already exists for this type
    DELETE_SUBSCRIPTION_TEMPLATE_ERROR = "A177"  # 500 — Delete subscription template error
    RESERVED_TEMPLATE_CANNOT_BE_DELETED = "A178"  # 400 — Reserved template cannot be deleted
    CREATE_SUBSCRIPTION_TEMPLATE_ERROR = "A179"  # 500 — Create subscription template error
    TEMPLATE_TYPE_NOT_ALLOWED = "A180"  # 400 — Template type not allowed
    GET_EXTERNAL_SQUADS_ERROR = "A181"  # 500 — Get external squads error
    EXTERNAL_SQUAD_NOT_FOUND = "A182"  # 404 — External squad not found
    CREATE_EXTERNAL_SQUAD_ERROR = "A183"  # 500 — Create external squad error
    UPDATE_EXTERNAL_SQUAD_ERROR = "A184"  # 500 — Update external squad error
    DELETE_EXTERNAL_SQUAD_ERROR = "A185"  # 500 — Delete external squad error
    ADD_USERS_TO_EXTERNAL_SQUAD_ERROR = "A186"  # 500 — Add users to external squad error
    REMOVE_USERS_FROM_EXTERNAL_SQUAD_ERROR = "A187"  # 500 — Remove users from external squad error
    GET_EXTERNAL_SQUAD_BY_UUID_ERROR = "A188"  # 500 — Get external squad by UUID error
    EXTERNAL_SQUAD_NAME_ALREADY_EXISTS = "A189"  # 400 — External squad name already exists
    NAME_OR_TEMPLATES_REQUIRED = "A190"  # 400 — Name or templates are required
    PASSKEY_NOT_FOUND = "A191"  # 404 — Passkey not found
    GET_REMNAWAVE_SETTINGS_ERROR = "A192"  # 500 — Get Remnawave settings error
    UPDATE_REMNAWAVE_SETTINGS_ERROR = "A193"  # 500 — Update Remnawave settings error
    PASSKEYS_NOT_CONFIGURED = "A194"  # 400 — Passkeys not configured
    PASSKEYS_NOT_ENABLED = "A195"  # 400 — Passkeys not enabled. Please enable it first.
    GENERATE_PASSKEY_REGISTRATION_OPTIONS = "A196"  # 500 — Generate passkey registration options error
    VERIFY_PASSKEY_REGISTRATION_ERROR = "A197"  # 500 — Verify passkey registration error
    GET_ACTIVE_PASSKEYS_ERROR = "A198"  # 500 — Get active passkeys error
    DELETE_PASSKEY_ERROR = "A199"  # 500 — Delete passkey error
    VALIDATE_REMNAWAVE_SETTINGS_ERROR = "A199"  # 500 — Validate Remnawave settings error
    GET_COMPUTED_CONFIG_PROFILE_BY_UUID_ERROR = "A200"  # 500 — Get computed config profile by UUID error
    RESET_NODE_TRAFFIC_ERROR = "A201"  # 500 — Reset node traffic error
    UPDATE_PASSKEY_ERROR = "A202"  # 500 — Update passkey error
    GENERIC_REORDER_ERROR = "A203"  # 500 — Generic reorder error
    HWID_DEVICE_NOT_FOUND = "A204"  # 404 — HWID device not found
    BULK_EXTEND_EXPIRATION_DATE_ERROR = "A205"  # 500 — Bulk extend expiration date error
    SUBSCRIPTION_PAGE_CONFIG_NOT_FOUND = "A206"  # 404 — Subscription page config not found
    GET_SUBSCRIPTION_PAGE_CONFIG_BY_UUID_ERROR = "A207"  # 500 — Get subscription page config by UUID error
    GET_ALL_SUBSCRIPTION_PAGE_CONFIGS_ERROR = "A208"  # 500 — Get all subscription page configs error
    RESERVED_CONFIG_NAME = "A209"  # 400 — Reserved config name
    CONFIG_NAME_ALREADY_EXISTS = "A210"  # 400 — Config name already exists
    UPDATE_SUBSCRIPTION_PAGE_CONFIG_ERROR = "A211"  # 500 — Update subscription page config error
    RESERVED_SUBPAGE_CONFIG_CANT_BE_DELETED = "A212"  # 400 — Reserved subpage config cannot be deleted
    DELETE_SUBSCRIPTION_PAGE_CONFIG_ERROR = "A213"  # 500 — Delete subscription page config error
    CREATE_SUBSCRIPTION_PAGE_CONFIG_ERROR = "A214"  # 500 — Create subscription page config error
    INVALID_SUBSCRIPTION_PAGE_CONFIG = "A215"  # 400 — Invalid subscription page config
    INVALID_REMNAWAVE_INJECTOR = "A216"  # 400 — Invalid Remnawave injector
    JOB_CREATION_FAILED = "A217"  # 500 — Job creation failed
    JOB_RESULT_FETCH_FAILED = "A218"  # 404 — Job result fetch failed or job not found
    CONNECTED_NODES_NOT_FOUND = "A219"  # 404 — Connected nodes not found
    GET_ALL_NODE_PLUGINS_ERROR = "A219"  # 500 — Get all node plugins error
    NODE_PLUGIN_NOT_FOUND = "A220"  # 404 — Node plugin not found
    GET_NODE_PLUGIN_BY_UUID_ERROR = "A221"  # 500 — Get node plugin by UUID error
    INVALID_NODE_PLUGIN_CONFIG = "A222"  # 400 — Invalid node plugin config
    NODE_PLUGIN_NAME_ALREADY_EXISTS = "A223"  # 400 — Node plugin name already exists
    UPDATE_NODE_PLUGIN_ERROR = "A224"  # 500 — Update node plugin error
    CREATE_NODE_PLUGIN_ERROR = "A225"  # 500 — Create node plugin error
    METADATA_NOT_FOUND = "A226"  # 404 — Metadata not found
    GET_TORRENT_BLOCKER_REPORTS_ERROR = "A227"  # 500 — Get torrent blocker reports error
    UPDATE_HOSTS_ERROR = "A228"  # 500 — Update hosts error
    INVALID_API_TOKEN_SCOPE = "A229"  # 400 — One or more provided API token scopes are invalid
    CREATE_INFRA_BILLING_NODE_MISSING_TARGET = "A230"  # 400 — Either nodeUuid or name must be provided
    CUSTOM_RAW_REMARK_VALIDATION_ERROR = "A231"  # 500 — Invalid custom raw remark
    GET_INTERNAL_SQUAD_USAGE_ERROR = "A232"  # 500 — Get internal squad usage error
    ADD_MANY_USERS_TO_INTERNAL_SQUAD_ERROR = "A233"  # 500 — Add many users to internal squad error
    REMOVE_MANY_USERS_FROM_INTERNAL_SQUAD_ERROR = "A234"  # 500 — Remove many users from internal squad error
    GET_STATS_DIGEST_INVALID_RANGE = "A235"  # 400 — Start date must be before or equal to end date
    GET_STATS_DIGEST_ERROR = "A236"  # 500 — Get stats digest error
    NODE_ERROR_WITH_MSG = "N001"  # 500 — 
    NODE_ERROR_500_WITH_MSG = "N002"  # 500 — 


#: HTTP-статус каждого кода ошибки согласно контракту.
ERROR_HTTP_CODES: "dict[str, int]" = {
    "A001": 500,
    "A002": 500,
    "A003": 401,
    "A004": 403,
    "A005": 500,
    "A006": 500,
    "A007": 404,
    "A008": 500,
    "A009": 500,
    "A010": 500,
    "A011": 404,
    "A012": 404,
    "A013": 500,
    "A014": 500,
    "A015": 500,
    "A016": 500,
    "A017": 500,
    "A018": 500,
    "A019": 400,
    "A020": 400,
    "A021": 400,
    "A022": 500,
    "A023": 500,
    "A024": 500,
    "A025": 404,
    "A026": 500,
    "A027": 500,
    "A028": 500,
    "A029": 400,
    "A030": 400,
    "A031": 500,
    "A032": 500,
    "A033": 400,
    "A034": 400,
    "A035": 500,
    "A036": 500,
    "A037": 500,
    "A038": 500,
    "A039": 500,
    "A040": 500,
    "A041": 500,
    "A042": 500,
    "A043": 500,
    "A044": 500,
    "A045": 400,
    "A046": 404,
    "A047": 500,
    "A048": 500,
    "A049": 500,
    "A050": 500,
    "A051": 500,
    "A052": 500,
    "A053": 500,
    "A054": 409,
    "A055": 500,
    "A056": 500,
    "A057": 500,
    "A058": 500,
    "A059": 500,
    "A060": 500,
    "A061": 500,
    "A062": 404,
    "A063": 404,
    "A064": 500,
    "A065": 404,
    "A066": 500,
    "A067": 500,
    "A068": 403,
    "A069": 500,
    "A070": 500,
    "A071": 404,
    "A072": 500,
    "A073": 500,
    "A074": 500,
    "A075": 500,
    "A076": 404,
    "A077": 500,
    "A078": 500,
    "A079": 500,
    "A080": 500,
    "A081": 500,
    "A084": 500,
    "A085": 500,
    "A086": 500,
    "A087": 500,
    "A088": 500,
    "A089": 500,
    # ErrorCode.INVALID_USER_STATUS_ERROR -> 400: код A089 переиспользован контрактом
    "A090": 500,
    "A091": 500,
    "A092": 500,
    "A093": 500,
    "A096": 500,
    "A097": 500,
    "A098": 400,
    "A099": 400,
    "A100": 500,
    "A101": 500,
    "A102": 500,
    "A103": 500,
    "A104": 500,
    "A105": 500,
    "A106": 500,
    "A107": 500,
    "A108": 500,
    "A109": 500,
    "A110": 500,
    "A111": 404,
    "A112": 500,
    "A113": 409,
    "A114": 409,
    "A115": 500,
    "A116": 500,
    "A117": 500,
    "A118": 404,
    "A119": 500,
    "A120": 409,
    "A121": 500,
    "A122": 500,
    "A123": 500,
    "A124": 404,
    "A125": 500,
    "A126": 500,
    "A127": 500,
    "A128": 404,
    "A129": 500,
    "A130": 500,
    "A131": 500,
    "A132": 500,
    "A133": 500,
    "A134": 500,
    "A135": 500,
    "A136": 500,
    "A137": 500,
    "A138": 500,
    "A139": 500,
    "A140": 500,
    "A141": 500,
    "A142": 500,
    "A143": 500,
    "A144": 400,
    "A145": 400,
    "A146": 500,
    "A147": 404,
    "A148": 500,
    "A149": 400,
    "A150": 500,
    "A151": 500,
    "A152": 400,
    "A153": 400,
    "A154": 500,
    "A155": 500,
    "A156": 500,
    "A157": 500,
    "A158": 500,
    "A159": 500,
    "A160": 500,
    "A161": 500,
    "A162": 404,
    "A163": 500,
    "A164": 400,
    "A165": 500,
    "A166": 400,
    "A167": 400,
    "A168": 500,
    "A169": 500,
    "A170": 404,
    "A171": 500,
    "A172": 400,
    "A173": 400,
    "A174": 400,
    "A175": 400,
    "A176": 400,
    "A177": 500,
    "A178": 400,
    "A179": 500,
    "A180": 400,
    "A181": 500,
    "A182": 404,
    "A183": 500,
    "A184": 500,
    "A185": 500,
    "A186": 500,
    "A187": 500,
    "A188": 500,
    "A189": 400,
    "A190": 400,
    "A191": 404,
    "A192": 500,
    "A193": 500,
    "A194": 400,
    "A195": 400,
    "A196": 500,
    "A197": 500,
    "A198": 500,
    "A199": 500,
    # ErrorCode.VALIDATE_REMNAWAVE_SETTINGS_ERROR -> 500: код A199 переиспользован контрактом
    "A200": 500,
    "A201": 500,
    "A202": 500,
    "A203": 500,
    "A204": 404,
    "A205": 500,
    "A206": 404,
    "A207": 500,
    "A208": 500,
    "A209": 400,
    "A210": 400,
    "A211": 500,
    "A212": 400,
    "A213": 500,
    "A214": 500,
    "A215": 400,
    "A216": 400,
    "A217": 500,
    "A218": 404,
    "A219": 404,
    # ErrorCode.GET_ALL_NODE_PLUGINS_ERROR -> 500: код A219 переиспользован контрактом
    "A220": 404,
    "A221": 500,
    "A222": 400,
    "A223": 400,
    "A224": 500,
    "A225": 500,
    "A226": 404,
    "A227": 500,
    "A228": 500,
    "A229": 400,
    "A230": 400,
    "A231": 500,
    "A232": 500,
    "A233": 500,
    "A234": 500,
    "A235": 400,
    "A236": 500,
    "N001": 500,
    "N002": 500,
}

#: Сообщение по умолчанию для каждого кода ошибки.
ERROR_MESSAGES: "dict[str, str]" = {
    "A001": "Server error",
    "A002": "Login error",
    "A003": "Unauthorized",
    "A004": "Forbidden role error",
    "A005": "Create API token error",
    "A006": "Delete API token error",
    "A007": "Requested token not found",
    "A008": "Find all API tokens error",
    "A009": "Get public key error",
    "A010": "Enable node error",
    "A011": "Node not found",
    "A012": "Configuration not found",
    "A013": "Error updating configuration",
    "A014": "Error retrieving configuration",
    "A015": "Delete many inbounds error",
    "A016": "Create many inbounds error",
    "A017": "Find all inbounds error",
    "A018": "Failed to create user",
    "A019": "User username already exists",
    "A020": "User short UUID already exists",
    "A021": "User subscription UUID already exists",
    "A022": "User creation successful, but inbound creation failed. User not created.",
    "A023": "User creation successful, but failed to get created user with inbounds.",
    "A024": "Get all users error",
    "A025": "User not found",
    "A026": "Get user by error",
    "A027": "Revoke user subscription error",
    "A028": "Disable user error",
    "A029": "User already disabled",
    "A030": "User already enabled",
    "A031": "Enable user error",
    "A032": "Create node error",
    "A033": "Node name already exists",
    "A034": "Node address already exists",
    "A035": "Restart node error",
    "A036": "Get config with users error",
    "A037": "Delete user error",
    "A038": "Update node error",
    "A039": "Update user error",
    "A040": "Increment used traffic error",
    "A041": "Get all nodes error",
    "A042": "Get one node error",
    "A043": "Delete node error",
    "A044": "Create host error",
    "A045": "Host remark already exists",
    "A046": "Host not found",
    "A047": "Delete host error",
    "A048": "Get user stats error",
    "A049": "Update user with inbounds error",
    "A050": "Get all hosts error",
    "A051": "Reorder hosts error",
    "A052": "Update host error",
    "A053": "Create config error",
    "A054": "Enabled nodes not found",
    "A055": "Get nodes usage by range error",
    "A056": "Reset user traffic error",
    "A057": "Reorder nodes error",
    "A058": "Get all inbounds error",
    "A059": "Bulk delete users by status error",
    "A060": "Update inbound error",
    "A061": "Config validation error",
    "A062": "Users not found",
    "A063": "User with specified params not found",
    "A064": "Update exceeded traffic users error",
    "A065": "Admin not found",
    "A066": "Create admin error",
    "A067": "Get auth status error",
    "A068": "Forbidden",
    "A069": "Disable node error",
    "A070": "Get one host error",
    "A071": "Subscription settings not found",
    "A072": "Get subscription settings error",
    "A073": "Update subscription settings error",
    "A074": "Add inbound to users error",
    "A075": "Remove inbound from users error",
    "A076": "Inbound not found",
    "A077": "Add inbound to nodes error",
    "A078": "Remove inbound from nodes error",
    "A079": "Delete hosts error",
    "A080": "Bulk enable hosts error",
    "A081": "Bulk disable hosts error",
    "A084": "Bulk delete users by UUID error",
    "A085": "Bulk revoke users subscription error",
    "A086": "Bulk reset user traffic error",
    "A087": "Bulk update users error",
    "A088": "Bulk add inbounds to users error",
    "A089": "Bulk update all users error",
    "A090": "Keypair creation error",
    "A091": "Get user usage by range error",
    "A092": "Keypair not found. Restart app.",
    "A093": "Activate all inbounds error",
    "A096": "Create hwid user device error",
    "A097": "Check hwid exists error",
    "A098": "User hwid device already exists",
    "A099": "User hwid device limit reached",
    "A100": "Get user hwid devices error",
    "A101": "Delete hwid user device error",
    "A102": "Upsert hwid user device error",
    "A103": "Get all tags error",
    "A104": "Getting all subscriptions error",
    "A105": "Trigger threshold notification error",
    "A106": "Bulk delete by status error",
    "A107": "Clean old usage records error",
    "A108": "Vacuum table error",
    "A109": "Get config profiles error",
    "A110": "Get config profile by UUID error",
    "A111": "Config profile not found",
    "A112": "Create config profile error",
    "A113": "Inbounds with same tag already exists in database. Inbound tags must be unique.",
    "A114": "Config profile name already exists in database. Config profile names must be unique.",
    "A115": "Get inbounds by profile UUID error",
    "A116": "Get internal squads error",
    "A117": "Get internal squad by UUID error",
    "A118": "Internal squad not found",
    "A119": "Create internal squad error",
    "A120": "Internal squad name already exists",
    "A121": "Update internal squad error",
    "A122": "Delete internal squad error",
    "A123": "Create user with internal squad error",
    "A124": "Config profile inbound not found in specified profile",
    "A125": "Get user accessible nodes error",
    "A126": "Get infra providers error",
    "A127": "Get infra provider by UUID error",
    "A128": "Infra provider not found",
    "A129": "Delete infra provider by UUID error",
    "A130": "Create infra provider error",
    "A131": "Update infra provider error",
    "A132": "Create infra billing history record error",
    "A133": "Get infra billing history records error",
    "A134": "Delete infra billing history record by UUID error",
    "A135": "Get billing nodes error",
    "A136": "Update infra billing node error",
    "A137": "Create infra billing node error",
    "A138": "Delete infra billing node by UUID error",
    "A139": "Get billing nodes for notifications error",
    "A140": "Add users to internal squad error",
    "A141": "Internal squad bulk actions error",
    "A142": "Remove users from internal squad error",
    "A143": "Delete config profile by UUID error",
    "A144": "This name is reserved by Remnawave. Please use a different name.",
    "A145": "This name is reserved by Remnawave. Please use a different name.",
    "A146": "Update config profile error",
    "A147": "OAuth2 provider not found",
    "A148": "OAuth2 authorize error",
    "A149": "Node is disabled",
    "A150": "Sync active profile error",
    "A151": "Get all host tags error",
    "A152": "Name or config is required",
    "A153": "Name or inbounds is required",
    "A154": "Get internal squad accessible nodes error",
    "A155": "Delete hwid user devices error",
    "A156": "Create user subscription request history error",
    "A157": "Get user subscription request history error",
    "A158": "Get all hwid devices error",
    "A159": "Get hwid devices stats error",
    "A160": "Get user subscription request history stats error",
    "A161": "Get snippets error",
    "A162": "Snippet not found",
    "A163": "Delete snippet by name error",
    "A164": "Snippet name already exists",
    "A165": "Update snippet error",
    "A166": "Snippet cannot be empty",
    "A167": "Snippet cannot contain empty objects",
    "A168": "Get all subscription templates error",
    "A169": "Get subscription template by UUID error",
    "A170": "Subscription template not found",
    "A171": "Update subscription template error",
    "A172": "This name is reserved. Please use a different name.",
    "A173": "Template JSON is not allowed for YAML template",
    "A174": "Template YAML is not allowed for JSON template",
    "A175": "Template JSON and YAML cannot be updated simultaneously",
    "A176": "Template name already exists for this type",
    "A177": "Delete subscription template error",
    "A178": "Reserved template cannot be deleted",
    "A179": "Create subscription template error",
    "A180": "Template type not allowed",
    "A181": "Get external squads error",
    "A182": "External squad not found",
    "A183": "Create external squad error",
    "A184": "Update external squad error",
    "A185": "Delete external squad error",
    "A186": "Add users to external squad error",
    "A187": "Remove users from external squad error",
    "A188": "Get external squad by UUID error",
    "A189": "External squad name already exists",
    "A190": "Name or templates are required",
    "A191": "Passkey not found",
    "A192": "Get Remnawave settings error",
    "A193": "Update Remnawave settings error",
    "A194": "Passkeys not configured",
    "A195": "Passkeys not enabled. Please enable it first.",
    "A196": "Generate passkey registration options error",
    "A197": "Verify passkey registration error",
    "A198": "Get active passkeys error",
    "A199": "Delete passkey error",
    "A200": "Get computed config profile by UUID error",
    "A201": "Reset node traffic error",
    "A202": "Update passkey error",
    "A203": "Generic reorder error",
    "A204": "HWID device not found",
    "A205": "Bulk extend expiration date error",
    "A206": "Subscription page config not found",
    "A207": "Get subscription page config by UUID error",
    "A208": "Get all subscription page configs error",
    "A209": "Reserved config name",
    "A210": "Config name already exists",
    "A211": "Update subscription page config error",
    "A212": "Reserved subpage config cannot be deleted",
    "A213": "Delete subscription page config error",
    "A214": "Create subscription page config error",
    "A215": "Invalid subscription page config",
    "A216": "Invalid Remnawave injector",
    "A217": "Job creation failed",
    "A218": "Job result fetch failed or job not found",
    "A219": "Connected nodes not found",
    "A220": "Node plugin not found",
    "A221": "Get node plugin by UUID error",
    "A222": "Invalid node plugin config",
    "A223": "Node plugin name already exists",
    "A224": "Update node plugin error",
    "A225": "Create node plugin error",
    "A226": "Metadata not found",
    "A227": "Get torrent blocker reports error",
    "A228": "Update hosts error",
    "A229": "One or more provided API token scopes are invalid",
    "A230": "Either nodeUuid or name must be provided",
    "A231": "Invalid custom raw remark",
    "A232": "Get internal squad usage error",
    "A233": "Add many users to internal squad error",
    "A234": "Remove many users from internal squad error",
    "A235": "Start date must be before or equal to end date",
    "A236": "Get stats digest error",
    "N001": "",
    "N002": "",
}
