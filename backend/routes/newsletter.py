from fastapi import APIRouter, HTTPException, status
from fastapi.responses import JSONResponse
from pydantic import ValidationError
from models import NewsletterSubscription, NewsletterResponse
from database import db_manager

# Create router for newsletter endpoints
router = APIRouter(prefix="/newsletter", tags=["newsletter"])

@router.post(
    "/subscribe", 
    response_model=NewsletterResponse,
    status_code=status.HTTP_200_OK,
    responses={
        200: {
            "description": "Successful subscription or already subscribed",
            "content": {
                "application/json": {
                    "examples": {
                        "successful_subscription": {
                            "summary": "Successful new subscription",
                            "value": {
                                "success": True,
                                "message": "Successfully subscribed to newsletter!",
                                "email": "user@example.com"
                            }
                        },
                        "already_subscribed": {
                            "summary": "Email already subscribed",
                            "value": {
                                "success": False,
                                "message": "You are already subscribed.",
                                "email": "user@example.com"
                            }
                        },
                        "database_unavailable": {
                            "summary": "Database temporarily unavailable",
                            "value": {
                                "success": True,
                                "message": "Subscription received (database temporarily unavailable)",
                                "email": "user@example.com"
                            }
                        }
                    }
                }
            }
        },
        422: {
            "description": "Validation Error - Invalid email format",
            "content": {
                "application/json": {
                    "example": {
                        "detail": [
                            {
                                "type": "value_error",
                                "loc": ["body", "email"],
                                "msg": "value is not a valid email address: There must be something after the @-sign.",
                                "input": "user@",
                                "ctx": {
                                    "reason": "There must be something after the @-sign."
                                }
                            }
                        ]
                    }
                }
            }
        },
        500: {
            "description": "Internal Server Error",
            "content": {
                "application/json": {
                    "example": {
                        "detail": "Internal server error: Connection failed"
                    }
                }
            }
        }
    },
    summary="Subscribe to Newsletter",
    description="""
    Subscribe an email address to the newsletter.
    
    **Request Body:**
    - `email`: Valid email address (required)
    - `name`: Optional subscriber name
    
    **Response Scenarios:**
    - **Success (new subscription)**: Returns success=true with confirmation message
    - **Already subscribed**: Returns success=false indicating email is already registered
    - **Database issues**: Returns success=true but notes database unavailability
    - **Invalid email**: Returns 422 validation error with specific email format issue
    
    **Email Validation:**
    The email field uses strict validation and will reject:
    - Invalid email formats
    - Missing @ symbol
    - Missing domain parts
    - Invalid characters
    """
)
async def subscribe_to_newsletter(subscription: NewsletterSubscription):
    """
    Subscribe an email to the newsletter.
    
    Args:
        subscription: NewsletterSubscription model containing email and optional name
    
    Returns:
        NewsletterResponse with success status and message
    """
    try:
        # Save to Supabase database if available
        if db_manager.is_connected():
            try:
                await db_manager.save_newsletter_subscription(
                    email=subscription.email,
                    name=subscription.name
                )
                
                return NewsletterResponse(
                    success=True,
                    message="Successfully subscribed to newsletter!",
                    email=subscription.email
                )
            except Exception as db_error:
                # Check if it's a duplicate email error (unique constraint violation)
                error_str = str(db_error)
                
                # Handle Supabase/PostgreSQL unique constraint violation
                if ("23505" in error_str or 
                    "duplicate key value violates unique constraint" in error_str or
                    "newsletter_subscribers_email_key" in error_str or
                    "already exists" in error_str):
                    
                    print(f"Duplicate subscription attempt for email: {subscription.email}")
                    return NewsletterResponse(
                        success=False,
                        message="You are already subscribed.",
                        email=subscription.email
                    )
                
                # If database insert fails for other reasons, log the error but still return success
                print(f"Database error: {db_error}")
                return NewsletterResponse(
                    success=True,
                    message="Subscription received (database temporarily unavailable)",
                    email=subscription.email
                )
        else:
            # No database connection, just validate and return success
            return NewsletterResponse(
                success=True,
                message="Subscription received (database not configured)",
                email=subscription.email
            )

    except ValidationError as e:
        raise HTTPException(
            status_code=400,
            detail=f"Validation error: {str(e)}"
        )
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Internal server error: {str(e)}"
        )
