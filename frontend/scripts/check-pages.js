#!/usr/bin/env node
/**
 * 页面健康检查脚本
 * 检查所有页面是否可访问、是否有错误
 */

const http = require('http');

const BASE_URL = 'http://localhost:3000';

const pages = [
  { path: '/', name: '首页' },
  { path: '/login', name: '登录页' },
  { path: '/profile', name: '个人中心' },
  { path: '/billing', name: '会员充值' },
  { path: '/settings', name: '账号设置' },
  { path: '/gallery', name: '作品展示' },
  { path: '/api/auth/session', name: 'Session API' },
  { path: '/api/auth/providers', name: 'Providers API' },
];

const results = {
  passed: [],
  failed: [],
  warnings: [],
};

async function checkPage(page) {
  return new Promise((resolve) => {
    const url = BASE_URL + page.path;
    const startTime = Date.now();
    
    http.get(url, (res) => {
      const elapsed = Date.now() - startTime;
      let body = '';
      
      res.on('data', chunk => body += chunk);
      res.on('end', () => {
        const result = {
          ...page,
          status: res.statusCode,
          elapsed,
          size: body.length,
        };
        
        // 检查状态码
        if (res.statusCode >= 200 && res.statusCode < 400) {
          // 只检查真正的严重错误
          if (body.includes('Internal Server Error') || body.includes('Application error')) {
            result.error = '页面包含服务器错误';
            results.failed.push(result);
          } else {
            // 页面正常
            results.passed.push(result);
          }
        } else if (res.statusCode === 302 || res.statusCode === 307) {
          result.redirect = res.headers.location;
          results.warnings.push(result);
        } else {
          result.error = `HTTP ${res.statusCode}`;
          results.failed.push(result);
        }
        
        resolve(result);
      });
    }).on('error', (err) => {
      results.failed.push({
        ...page,
        error: err.message,
      });
      resolve();
    });
  });
}

async function checkAPI() {
  const apis = [
    { path: '/api/auth/session', name: 'Session' },
    { path: '/api/auth/providers', name: 'Providers' },
  ];
  
  for (const api of apis) {
    await checkPage(api);
  }
}

async function main() {
  console.log('🔍 开始检查页面...\n');
  console.log('=' .repeat(60));
  
  for (const page of pages) {
    process.stdout.write(`检查 ${page.name} (${page.path})... `);
    const result = await checkPage(page);
    
    if (results.passed.includes(result)) {
      console.log(`✅ ${result.status} (${result.elapsed}ms)`);
    } else if (results.warnings.includes(result)) {
      console.log(`⚠️ 重定向到 ${result.redirect}`);
    } else {
      console.log(`❌ ${result.error || '失败'}`);
    }
  }
  
  console.log('\n' + '='.repeat(60));
  console.log('\n📊 检查结果汇总:\n');
  
  console.log(`✅ 通过: ${results.passed.length}`);
  results.passed.forEach(r => console.log(`   - ${r.name}: ${r.status} (${r.elapsed}ms, ${Math.round(r.size/1024)}KB)`));
  
  if (results.warnings.length > 0) {
    console.log(`\n⚠️ 警告: ${results.warnings.length}`);
    results.warnings.forEach(r => console.log(`   - ${r.name}: 重定向到 ${r.redirect}`));
  }
  
  if (results.failed.length > 0) {
    console.log(`\n❌ 失败: ${results.failed.length}`);
    results.failed.forEach(r => console.log(`   - ${r.name}: ${r.error}`));
  }
  
  console.log('\n' + '='.repeat(60));
  
  // 返回退出码
  process.exit(results.failed.length > 0 ? 1 : 0);
}

main().catch(console.error);
