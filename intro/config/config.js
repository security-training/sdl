"use strict";
// For recover password
var bookmark = {
    reset: unescape(window.location.search.replace("?reset_password=", "")),
    inviter: "https://prod-global-webapp-proxy.nubank.com.br/api/inviter/:slug",
    prospect_linkedin: "https://prod-global-webapp-proxy.nubank.com.br/api/prospects/:id/linkedin",
    discovery: "https://prod-global-webapp-proxy.nubank.com.br/api/discovery",
    auth_discovery: "https://prod-global-webapp-proxy.nubank.com.br/api/app/discovery",
    new_account_recovery_confirm: "https://prod-global-webapp-proxy.nubank.com.br/api/account-recovery/confirm/:prototype",
    hypermedia: "https://prod-auth.nubank.com.br/api/admin/users/:id/hypermedia",
    mgm_page: "https://nubank.com.br/indicacao/"
  },
  env = "prod",
  tokens = {
    linkedin: "78t1wvswkyr7br",
    ga_mgm: "UA-54526048-3",
    amplitude: "a042652874b2ef595b4224f644c54fa7",
    gtm: "GTM-TGCKXJT"
  },
  sentry = {
    dsn: "https://b46eec158d54413a999a8e40b80bc0b6@sentry.io/59090",
    config: {
      environment: window.env,
      ignoreErrors: [
        'missing ] after element list',
        'Expected either a closing \']\' or a \',\' following an array element',
        'TypeError: a is undefined',
        /__gCrWeb/,
        'measurePositions',
        'vid_mate_check',
        // default ignorables
        'top.GLOBALS',
        'originalCreateNotification',
        'MyApp_RemoveAllHighlights',
        'jigsaw is not defined',
        'ComboSearch is not defined',
        'http://loading.retry.widdit.com/',
        'atomicFindClose',
        'fb_xd_fragment',
        'bmi_SafeAddOnload',
        'EBCallBackMessageReceived',
        'conduitPage'
      ],
      ignoreUrls: [
        /speculatedurethras\.com/,
        /graph\.facebook\.com/i,
        /connect\.facebook\.net\/en_US\/all\.js/i,
        /extensions\//i,
        /^chrome:\/\//i,
        /127\.0\.0\.1:4001\/isrunning/i,
        /webappstoolbarba\.texthelp\.com\//i,
        /metrics\.itunes\.apple\.com\.edgesuite\.net\//i
      ]
    }
  },
  linkedin = {
    scopes: 'r_basicprofile r_emailaddress',
    lang: 'pt_BR'
  },
  client_info = {
    "name": "Nubank",
    "uri": "https://www.nubank.com.br"
  };

if (typeof angular !== 'undefined') {
  angular.module("envConfig", [])

  .constant("ENV", "prod")

  .constant("CONFIG", {
    "appName": "WEB-APP",
    "bookmarks": window.bookmark,
    "tokens": window.tokens
  });
}
