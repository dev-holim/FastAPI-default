from app import create_app, lifespan_

app = create_app(lifespan=lifespan_)


@app.get(path='/health')
async def health_check_api():
    return {
        'status': 'ok'
    }


if __name__ == '__main__':
    import uvicorn

    uvicorn.run(
        app=app,
        host='0.0.0.0',
        port=8000,
    )
