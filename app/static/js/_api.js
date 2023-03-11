export async function post(url, body) {
  try {
    const query = await fetch(`${window.location.origin}${url}`, {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify(body),
    });

    const data = await query.json();
    const status = query.status;

    return { status, data };
  } catch (error) {
    throw new Error(error.message);
  }
}

export async function get(url) {
  try {
    const query = await fetch(`${window.location.origin}${url}`, {
      method: "GET",
      headers: {
        "Content-Type": "application/json",
      },
    });

    const data = await query.json();
    const status = query.status;

    return { status, data };
  } catch (error) {
    throw new Error(error.message);
  }
}

export async function patch(url, body) {
  try {
    const query = await fetch(`${window.location.origin}${url}`, {
      method: "PATCH",
      body: JSON.stringify(body),
      headers: {
        "Content-Type": "application/json",
      },
    });

    const status = query.status;

    return status;
  } catch (error) {
    throw new Error(error.message);
  }
}

export async function remove(url, item) {
  try {
    const query = await fetch(`${window.location.origin}${url}/${item}`, {
      method: "DELETE",
      headers: {
        "Content-Type": "application/json",
      },
    });

    const status = query.status;

    return status;
  } catch (error) {
    throw new Error(error.message);
  }
}
