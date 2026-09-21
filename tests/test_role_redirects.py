from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait


def test_hr_recruiter_login_redirects_to_hr_dashboard(live_server, driver):
    driver.get(f"{live_server}/index.html")
    wait = WebDriverWait(driver, 15)

    driver.execute_script(
        """
        window.supabaseClient = {
          auth: {
            getSession: async () => ({ data: { session: null } }),
            signInWithPassword: async ({ email, password }) => ({
              data: { user: { id: 'user-123', email } },
              error: null,
            }),
            signOut: async () => ({ error: null }),
          },
          from: (table) => ({
            select: (field) => ({
              eq: (column, value) => ({
                single: async () => {
                  if (table === 'user_roles') {
                    return { data: { role_id: 1 }, error: null };
                  }
                  if (table === 'roles') {
                    return { data: { role_name: 'hr_recruiter' }, error: null };
                  }
                  return { data: null, error: null };
                }
              })
            })
          })
        };
        """
    )

    wait.until(EC.presence_of_element_located((By.ID, "loginForm")))
    driver.find_element(By.ID, "email").clear()
    driver.find_element(By.ID, "email").send_keys("hr@example.com")
    driver.find_element(By.ID, "password").clear()
    driver.find_element(By.ID, "password").send_keys("Password123!")
    driver.find_element(By.ID, "loginBtn").click()

    WebDriverWait(driver, 15).until(
        lambda d: d.current_url.endswith("dashboards/hr-dashboard.html")
    )

    assert driver.current_url.endswith("dashboards/hr-dashboard.html")
    assert driver.execute_script("return localStorage.getItem('userRole')") == "hr_recruiter"


def test_interviewer_login_redirects_to_interviewer_dashboard(live_server, driver):
    driver.get(f"{live_server}/index.html")
    wait = WebDriverWait(driver, 15)

    driver.execute_script(
        """
        window.supabaseClient = {
          auth: {
            getSession: async () => ({ data: { session: null } }),
            signInWithPassword: async ({ email, password }) => ({
              data: { user: { id: 'interviewer-789', email } },
              error: null,
            }),
            signOut: async () => ({ error: null }),
          },
          from: (table) => ({
            select: (field) => ({
              eq: (column, value) => ({
                single: async () => {
                  if (table === 'user_roles') {
                    return { data: { role_id: 2 }, error: null };
                  }
                  if (table === 'roles') {
                    return { data: { role_name: 'interviewer' }, error: null };
                  }
                  return { data: null, error: null };
                }
              })
            })
          })
        };
        """
    )

    wait.until(EC.presence_of_element_located((By.ID, "loginForm")))
    driver.find_element(By.ID, "email").clear()
    driver.find_element(By.ID, "email").send_keys("interviewer@example.com")
    driver.find_element(By.ID, "password").clear()
    driver.find_element(By.ID, "password").send_keys("Password123!")
    driver.find_element(By.ID, "loginBtn").click()

    WebDriverWait(driver, 15).until(
        lambda d: d.current_url.endswith("dashboards/interviewer-dashboard.html")
    )

    assert driver.current_url.endswith("dashboards/interviewer-dashboard.html")
    assert driver.execute_script("return localStorage.getItem('userRole')") == "interviewer"


def test_hiring_manager_login_redirects_to_hiring_manager_dashboard(live_server, driver):
    driver.get(f"{live_server}/index.html")
    wait = WebDriverWait(driver, 15)

    driver.execute_script(
        """
        window.supabaseClient = {
          auth: {
            getSession: async () => ({ data: { session: null } }),
            signInWithPassword: async ({ email, password }) => ({
              data: { user: { id: 'manager-456', email } },
              error: null,
            }),
            signOut: async () => ({ error: null }),
          },
          from: (table) => ({
            select: (field) => ({
              eq: (column, value) => ({
                single: async () => {
                  if (table === 'user_roles') {
                    return { data: { role_id: 3 }, error: null };
                  }
                  if (table === 'roles') {
                    return { data: { role_name: 'hiring_manager' }, error: null };
                  }
                  return { data: null, error: null };
                }
              })
            })
          })
        };
        """
    )

    wait.until(EC.presence_of_element_located((By.ID, "loginForm")))
    driver.find_element(By.ID, "email").clear()
    driver.find_element(By.ID, "email").send_keys("hiringmanager@example.com")
    driver.find_element(By.ID, "password").clear()
    driver.find_element(By.ID, "password").send_keys("Password123!")
    driver.find_element(By.ID, "loginBtn").click()

    WebDriverWait(driver, 15).until(
        lambda d: d.current_url.endswith("dashboards/hiring-manager-dashboard.html")
    )

    assert driver.current_url.endswith("dashboards/hiring-manager-dashboard.html")
    assert driver.execute_script("return localStorage.getItem('userRole')") == "hiring_manager"


def test_management_login_redirects_to_management_dashboard(live_server, driver):
    driver.get(f"{live_server}/index.html")
    wait = WebDriverWait(driver, 15)

    driver.execute_script(
        """
        window.supabaseClient = {
          auth: {
            getSession: async () => ({ data: { session: null } }),
            signInWithPassword: async ({ email, password }) => ({
              data: { user: { id: 'manager-456', email } },
              error: null,
            }),
            signOut: async () => ({ error: null }),
          },
          from: (table) => ({
            select: (field) => ({
              eq: (column, value) => ({
                single: async () => {
                  if (table === 'user_roles') {
                    return { data: { role_id: 4 }, error: null };
                  }
                  if (table === 'roles') {
                    return { data: { role_name: 'management' }, error: null };
                  }
                  return { data: null, error: null };
                }
              })
            })
          })
        };
        """
    )

    wait.until(EC.presence_of_element_located((By.ID, "loginForm")))
    driver.find_element(By.ID, "email").clear()
    driver.find_element(By.ID, "email").send_keys("management@example.com")
    driver.find_element(By.ID, "password").clear()
    driver.find_element(By.ID, "password").send_keys("Password123!")
    driver.find_element(By.ID, "loginBtn").click()

    WebDriverWait(driver, 15).until(
        lambda d: d.current_url.endswith("dashboards/management-dashboard.html")
    )

    assert driver.current_url.endswith("dashboards/management-dashboard.html")
    assert driver.execute_script("return localStorage.getItem('userRole')") == "management"
